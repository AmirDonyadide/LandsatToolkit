import os
import shutil
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

class SceneOperations:
    """
    Handles scene processing and index calculation operations.
    """

    def __init__(self, input_folder):
        """
        Initialize the SceneOperations with the input folder path.

        Args:
            input_folder (str): Path to the input folder containing raw satellite data.
        """
        self.input_folder = input_folder

    # Scene Processing Methods
    def organize_satellite_data(self, output_folder):
        """
        Organizes satellite data into the specified output folder.

        Args:
            output_folder (str): Path to the folder where organized data will be saved.
        """
        scene_files = {}

        # Scan the input folder for files
        for file_name in os.listdir(self.input_folder):
            file_path = os.path.join(self.input_folder, file_name)
            if not os.path.isfile(file_path):
                continue  # Skip directories

            satellite_type = self.detect_satellite_type(file_name)
            if not satellite_type:
                continue

            scene_id = "_".join(file_name.split("_")[:7])
            scene_files.setdefault(satellite_type, {}).setdefault(scene_id, []).append(file_path)

        # Create the output folder structure and copy files
        for satellite_type, scenes in scene_files.items():
            for scene_id, files in scenes.items():
                scene_folder = os.path.join(output_folder, satellite_type.upper(), scene_id)
                os.makedirs(scene_folder, exist_ok=True)
                for file_path in files:
                    shutil.copy(file_path, scene_folder)

        print("Satellite data organization complete.")

    def detect_satellite_type(self, file_name):
        """
        Detects the satellite type based on the file name.

        Args:
            file_name (str): Name of the file to analyze.

        Returns:
            str: Satellite type ("landsat 7", "landsat 8", "landsat 9") or None if not recognized.
        """
        file_name = file_name.lower()

        if "le07" in file_name:
            return "landsat7"
        elif "lc08" in file_name:
            return "landsat8"
        elif "lc09" in file_name:
            return "landsat9"

        print(f"Unsupported satellite type for file: {file_name}")
        return None

    def group_files_by_scene(self):
        """
        Groups files by scene based on satellite type.

        Returns:
            dict: Dictionary with scene IDs as keys and lists of file paths as values.
        """
        scenes = {}
        for file_name in os.listdir(self.input_folder):
            if file_name.startswith("."):
                continue  # Skip hidden files

            satellite_type = self.detect_satellite_type(file_name)
            if not satellite_type:
                continue

            scene_id = "_".join(file_name.split("_")[:7])
            scenes.setdefault(scene_id, []).append(os.path.join(self.input_folder, file_name))

        return scenes

    def create_band_matrices(self, scene_id):
        """
        Creates a band matrix for the scene.

        Args:
            scene_id (str): Scene ID to create band matrices for.

        Returns:
            np.ndarray: 3D NumPy array representing the stacked bands.
        """
        scene_files = self.group_files_by_scene().get(scene_id, [])
        band_arrays = []

        for file_path in scene_files:
            if "_sr_b" in file_path.lower():  # Look for specific band files
                try:
                    with rasterio.open(file_path) as src:
                        band_arrays.append(src.read(1))
                except Exception as e:
                    print(f"Error reading band file {file_path}: {e}")

        if not band_arrays:
            raise ValueError(f"No valid band files found for scene {scene_id}.")

        matrix = np.stack(band_arrays, axis=0)
        return matrix

    def calculate_and_save_index(self, band_matrix, index_type, satellite_type, output_file, B4=None):
        """
        Calculates an index for a given band matrix and saves it to a file.

        Args:
            band_matrix (np.ndarray): 3D NumPy array of band data.
            index_type (str): Type of index to calculate (e.g., "NDVI", "NDWI").
            satellite_type (str): Satellite type (e.g., "landsat7").
            output_file (str): Path to save the calculated index.
            B4 (str): Path to B4 file for specific calculations.

        Returns:
            None
        """

        # Select the calculation method
        if index_type == "NDVI":
            index = self.calculate_ndvi(band_matrix)
        elif index_type == "NDWI":
            index = self.calculate_ndwi(band_matrix)
        elif index_type == "NDBI":
            index = self.calculate_ndbi(band_matrix)
        elif index_type == "SAVI":
            index = self.calculate_savi(band_matrix)
        else:
            raise ValueError(f"Unsupported index type: {index_type}")

        # Validate the B4 reference file
        if B4 is None:
            raise FileNotFoundError(f"B4 reference file not found: {B4}")

        # Save the calculated index as a GeoTIFF
        with rasterio.open(B4) as src:
            meta = src.meta.copy()
            meta.update(count=1, dtype="float32")
            with rasterio.open(output_file, "w", **meta) as dst:
                dst.write(index.astype("float32"), 1)

    def calculate_ndvi(self, matrix):
        """
        Calculates the NDVI index.

        Args:
            matrix (np.ndarray): 3D NumPy array with band data.

        Returns:
            np.ndarray: NDVI values.
        """
        nir = matrix[4]  # Assuming Band 5 is NIR
        red = matrix[3]  # Assuming Band 4 is RED

        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = (nir - red) / (nir + red)
            ndvi = np.where(np.isfinite(ndvi), ndvi, 0)  # Replace NaN or Inf with 0
        return ndvi

    def calculate_ndwi(self, matrix):
        """
        Calculates the NDWI index.

        Args:
            matrix (np.ndarray): 3D NumPy array with band data.

        Returns:
            np.ndarray: NDWI values.
        """
        nir = matrix[4]
        green = matrix[2]  # Assuming Band 3 is GREEN

        with np.errstate(divide='ignore', invalid='ignore'):
            ndwi = (green - nir) / (green + nir)
            ndwi = np.where(np.isfinite(ndwi), ndwi, 0)
        return ndwi

    def calculate_ndbi(self, matrix):
        """
        Calculates the NDBI index.

        Args:
            matrix (np.ndarray): 3D NumPy array with band data.

        Returns:
            np.ndarray: NDBI values.
        """
        swir = matrix[5]  # Assuming Band 6 is SWIR
        nir = matrix[4]

        with np.errstate(divide='ignore', invalid='ignore'):
            ndbi = (swir - nir) / (swir + nir)
            ndbi = np.where(np.isfinite(ndbi), ndbi, 0)
        return ndbi

    def calculate_savi(self, matrix, L=0.5):
        """
        Calculates the SAVI index.

        Args:
            matrix (np.ndarray): 3D NumPy array with band data.
            L (float): Soil adjustment factor.

        Returns:
            np.ndarray: SAVI values.
        """
        nir = matrix[4]
        red = matrix[3]

        with np.errstate(divide='ignore', invalid='ignore'):
            savi = ((nir - red) / (nir + red + L)) * (1 + L)
            savi = np.where(np.isfinite(savi), savi, 0)
        return savi
    
    def reproject_scene(self, scene_id, target_crs, output_folder):
        """
        Reprojects all raster files in a scene to a specified CRS.

        Args:
            scene_id (str): Scene ID to reproject.
            target_crs (str): Target CRS (e.g., "EPSG:32633").
            output_folder (str): Path to the folder where reprojected files will be saved.

        Returns:
            None
        """
        print(f"Reprojecting scene: {scene_id} to {target_crs}...")
        scene_files = self.group_files_by_scene().get(scene_id, [])
        
        if not scene_files:
            print(f"No files found for scene {scene_id}. Skipping...")
            return

        for file_path in scene_files:
            if not file_path.lower().endswith(('.tif', '.geotiff')):
                continue  # Skip non-raster files

            try:
                with rasterio.open(file_path) as src:
                    transform, width, height = calculate_default_transform(
                        src.crs, target_crs, src.width, src.height, *src.bounds
                    )
                    meta = src.meta.copy()
                    meta.update({
                        "crs": target_crs,
                        "transform": transform,
                        "width": width,
                        "height": height,
                    })

                    output_file = os.path.join(output_folder, os.path.basename(file_path))
                    with rasterio.open(output_file, "w", **meta) as dst:
                        for i in range(1, src.count + 1):
                            reproject(
                                source=rasterio.band(src, i),
                                destination=rasterio.band(dst, i),
                                src_transform=src.transform,
                                src_crs=src.crs,
                                dst_transform=transform,
                                dst_crs=target_crs,
                                resampling=Resampling.nearest,
                            )

            except Exception as e:
                print(f"Error reprojecting file {file_path}: {e}")