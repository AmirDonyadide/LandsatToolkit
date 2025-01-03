import os
import shutil
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

class SceneProcessor:
    """
    Handles operations related to individual scenes.
    """

    def __init__(self, input_folder):
        """
        Initialize the SceneProcessor with the input folder path.

        Args:
            input_folder (str): Path to the input folder containing raw satellite data.
        """
        self.input_folder = input_folder

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

    def reproject_scene(self, scene_id, target_crs, output_folder=None):
        """
        Reprojects all raster files in a scene to a specified CRS and saves them to the output folder.

        Args:
            scene_id (str): Scene ID to reproject.
            target_crs (str): Target CRS (e.g., "EPSG:32633").
            output_folder (str, optional): Path to the folder where reprojected files will be saved.
                                        If None, a default folder will be created in the current directory.

        Returns:
            list: List of paths to the reprojected files.
        """

        # Group files for the scene
        scene_files = self.group_files_by_scene().get(scene_id, [])
        if not scene_files:
            print(f"No files found for scene {scene_id}. Skipping...")
            return []

        # Handle output folder
        if output_folder is None:
            output_folder = os.path.join(os.getcwd(), "reprojected", scene_id.upper())
        os.makedirs(output_folder, exist_ok=True)

        reprojected_files = []

        for file_path in scene_files:
            if not file_path.lower().endswith(('.tif', '.geotiff')):
                continue  # Skip non-raster files

            try:
                with rasterio.open(file_path) as src:
                    # Calculate transform and metadata for the target CRS
                    transform, width, height = calculate_default_transform(
                        src.crs, target_crs, src.width, src.height, *src.bounds
                    )
                    meta = src.meta.copy()
                    meta.update({"crs": target_crs, "transform": transform, "width": width, "height": height})

                    # Generate output file path
                    output_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_reprojected.tif"
                    output_file_path = os.path.join(output_folder, output_file_name)

                    # Reproject and save the raster
                    with rasterio.open(output_file_path, "w", **meta) as dst:
                        for i in range(1, src.count + 1):  # Loop through each band
                            reproject(
                                source=rasterio.band(src, i),
                                destination=rasterio.band(dst, i),
                                src_transform=src.transform,
                                src_crs=src.crs,
                                dst_transform=transform,
                                dst_crs=target_crs,
                                resampling=Resampling.nearest,
                            )

                    reprojected_files.append(output_file_path)

            except Exception as e:
                print(f"Error reprojecting file {file_path}: {e}")

        print(f"Reprojection complete for scene: {scene_id}.")
        return reprojected_files

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