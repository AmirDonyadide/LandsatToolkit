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
        
        Raises:
            ValueError: If the input folder does not exist or is not a directory.
        """
        try:
            if not os.path.exists(input_folder):
                raise ValueError(f"The input folder '{input_folder}' does not exist.")
            if not os.path.isdir(input_folder):
                raise ValueError(f"The path '{input_folder}' is not a directory.")
            self.input_folder = input_folder
            print(f"SceneOperations initialized with input folder: {input_folder}")
        except Exception as e:
            print(f"Error initializing SceneOperations: {e}")
            raise

    # Scene Processing Methods
    def organize_satellite_data(self, output_folder):
        """
        Organizes satellite data into the specified output folder.

        Args:
            output_folder (str): Path to the folder where organized data will be saved.
        
        Raises:
            ValueError: If the input folder does not contain any valid files for processing.
        """
        try:
            scene_files = {}

            # Scan the input folder for files
            print(f"Scanning input folder: {self.input_folder}")
            for file_name in os.listdir(self.input_folder):
                file_path = os.path.join(self.input_folder, file_name)

                # Skip directories and hidden/system files
                if not os.path.isfile(file_path):
                    continue

                # Detect the satellite type
                satellite_type = self.detect_satellite_type(file_name)
                if not satellite_type:
                    print(f"Skipping unsupported or unrecognized file: {file_name}")
                    continue

                # Group files by scene ID
                scene_id = "_".join(file_name.split("_")[:7])
                scene_files.setdefault(satellite_type, {}).setdefault(scene_id, []).append(file_path)

            # Raise an error if no valid files are found
            if not scene_files:
                raise ValueError("No valid satellite files found in the input folder.")

            # Create the output folder structure and copy files
            print(f"Organizing data into output folder: {output_folder}")
            for satellite_type, scenes in scene_files.items():
                for scene_id, files in scenes.items():
                    scene_folder = os.path.join(output_folder, satellite_type.upper(), scene_id)
                    os.makedirs(scene_folder, exist_ok=True)
                    for file_path in files:
                        shutil.copy(file_path, scene_folder)
                        print(f"Copied {file_path} to {scene_folder}")

            print("Satellite data organization complete.")

        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An error occurred while organizing satellite data: {e}")

    def detect_satellite_type(self, file_name):
        """
        Detects the satellite type based on the file name.

        Args:
            file_name (str): Name of the file to analyze.

        Returns:
            str: Satellite type ("landsat7", "landsat8", "landsat9") if recognized.
            None: If the satellite type is not recognized.

        Raises:
            ValueError: If the file_name is empty or None.
        """
        try:
            # Validate input
            if not file_name:
                raise ValueError("File name cannot be empty or None.")

            # Convert file name to lowercase for uniform comparison
            file_name = file_name.lower()

            # Detect satellite type based on naming patterns
            if "le07" in file_name:
                return "landsat7"
            elif "lc08" in file_name:
                return "landsat8"
            elif "lc09" in file_name:
                return "landsat9"

            # If no pattern matches, print and return None
            print(f"Unsupported satellite type for file: {file_name}")
            return None

        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An error occurred while detecting satellite type: {e}")

    def group_files_by_scene(self):
        """
        Groups files by scene based on satellite type.

        Returns:
            dict: Dictionary with scene IDs as keys and lists of file paths as values.
                  Example:
                  {
                      "LC08_L2SP_192029_20240716_20240722_02_T1": [
                          "path/to/file1.tif",
                          "path/to/file2.tif"
                      ],
                      ...
                  }

        Raises:
            FileNotFoundError: If the input folder does not exist.
            Exception: For other unexpected issues during file grouping.
        """
        try:
            # Validate that the input folder exists
            if not os.path.exists(self.input_folder):
                raise FileNotFoundError(f"Input folder '{self.input_folder}' does not exist.")

            scenes = {}
            file_list = os.listdir(self.input_folder)  # List all files in the input folder

            # Iterate over each file in the folder
            for file_name in file_list:
                # Skip hidden files (e.g., starting with ".")
                if file_name.startswith("."):
                    continue

                # Detect the satellite type
                satellite_type = self.detect_satellite_type(file_name)
                if not satellite_type:
                    print(f"Skipping file '{file_name}': Unrecognized satellite type.")
                    continue

                # Generate scene ID based on naming convention
                scene_id = "_".join(file_name.split("_")[:7])

                # Add the file to the corresponding scene in the dictionary
                full_path = os.path.join(self.input_folder, file_name)
                scenes.setdefault(scene_id, []).append(full_path)

            # Print summary of grouped scenes
            print(f"Grouped {len(scenes)} scenes from {len(file_list)} files.")
            return scenes

        except FileNotFoundError as fnfe:
            print(f"FileNotFoundError: {fnfe}")
        except Exception as e:
            print(f"An unexpected error occurred while grouping files: {e}")

    def create_band_matrices(self, scene_id):
        """
        Creates a 3D band matrix for the specified scene by stacking individual bands.

        Args:
            scene_id (str): Scene ID to create band matrices for.

        Returns:
            np.ndarray: 3D NumPy array representing the stacked bands.

        Raises:
            ValueError: If no valid band files are found for the specified scene.
            FileNotFoundError: If the scene ID does not exist in the grouped files.
        """
        try:
            # Get files associated with the scene ID
            scene_files = self.group_files_by_scene().get(scene_id, [])
            if not scene_files:
                raise FileNotFoundError(f"Scene ID '{scene_id}' not found in the input folder.")

            band_arrays = []

            # Iterate through the files and read band data
            for file_path in scene_files:
                if "_sr_b" in file_path.lower():  # Filter for specific band files
                    try:
                        with rasterio.open(file_path) as src:
                            band_arrays.append(src.read(1))  # Read the band data as a 2D array
                    except rasterio.errors.RasterioIOError as rio_err:
                        print(f"RasterioIOError: Could not read file '{file_path}': {rio_err}")
                    except Exception as e:
                        print(f"Error reading band file '{file_path}': {e}")

            # Raise an error if no valid band files were found
            if not band_arrays:
                raise ValueError(f"No valid band files found for scene '{scene_id}'.")

            # Stack the band arrays into a single 3D matrix
            matrix = np.stack(band_arrays, axis=0)
            print(f"Band matrix created for scene '{scene_id}'. Shape: {matrix.shape}")
            return matrix

        except FileNotFoundError as fnf_error:
            print(f"FileNotFoundError: {fnf_error}")
        except ValueError as val_error:
            print(f"ValueError: {val_error}")
        except Exception as e:
            print(f"An unexpected error occurred while creating band matrices: {e}")

    def calculate_and_save_index(self, band_matrix, index_type, satellite_type, output_file, B4=None, L=0.5):
        """
        Calculates a normalized difference index for a given band matrix and saves it to a GeoTIFF file.

        Args:
            band_matrix (np.ndarray): 3D NumPy array of band data.
            index_type (str): Type of index to calculate (e.g., "NDVI", "NDWI", "NDBI", "SAVI").
            satellite_type (str): Satellite type (e.g., "landsat7").
            output_file (str): Path to save the calculated index.
            B4 (str): Path to B4 file for metadata reference.
            L (float, optional): Soil adjustment factor for SAVI. Default is 0.5.

        Returns:
            None

        Raises:
            ValueError: If the index type is unsupported.
            FileNotFoundError: If the B4 reference file is not provided or invalid.
            Exception: For unexpected errors during index calculation or saving.
        """
        try:
            print(f"Calculating {index_type} for satellite type {satellite_type}...")

            # Check if the index is supported and call `normalized_difference`
            if index_type in ["NDVI", "NDWI", "NDBI", "SAVI"]:
                band_indices = {
                    "NDVI": (4, 3),  # NIR, RED
                    "NDWI": (2, 4),  # GREEN, NIR
                    "NDBI": (5, 4),  # SWIR, NIR
                    "SAVI": (4, 3),  # NIR, RED
                }
                numerator_band, denominator_band = band_indices[index_type]
                
                # Pass the L value only if the index is SAVI
                index = self.normalized_difference(
                    matrix=band_matrix,
                    numerator_band=numerator_band,
                    denominator_band=denominator_band,
                    index_type=index_type,
                    L=L if index_type == "SAVI" else None,
                )
            else:
                raise ValueError(f"Unsupported index type: {index_type}")
            
            # Validate the B4 reference file
            if B4 is None or not os.path.isfile(B4):
                raise FileNotFoundError(f"B4 reference file not found or invalid: {B4}")

            # Save the calculated index as a GeoTIFF
            with rasterio.open(B4) as src:
                meta = src.meta.copy()
                meta.update(count=1, dtype="float32")
                
                try:
                    with rasterio.open(output_file, "w", **meta) as dst:
                        dst.write(index.astype("float32"), 1)
                except Exception as save_error:
                    raise Exception(f"Error saving index to file '{output_file}': {save_error}")

            print(f"{index_type} index saved to {output_file}")

        except ValueError as ve:
            print(f"ValueError: {ve}")
            raise
        except FileNotFoundError as fnf_error:
            print(f"FileNotFoundError: {fnf_error}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while calculating or saving the index: {e}")
            raise

    def normalized_difference(self, matrix, numerator_band, denominator_band, index_type, L=0.5):
        """
        Calculates a normalized difference index for specified bands and standardizes values for each pixel.

        Args:
            matrix (np.ndarray): 3D NumPy array with band data.
            numerator_band (int): Index of the numerator band.
            denominator_band (int): Index of the denominator band.
            index_type (str): Type of index (e.g., NDVI, NDWI, NDBI, SAVI).
            L (float, optional): Soil adjustment factor for SAVI, default is 0.5.

        Returns:
            np.ndarray: Normalized difference index values clipped to the expected range.
        """
        try:
            numerator = matrix[numerator_band]
            denominator = matrix[denominator_band]

            # Handle SAVI calculation
            if index_type == "SAVI":
                with np.errstate(divide="ignore", invalid="ignore"):
                    index = ((numerator - denominator) / (numerator + denominator + L)) * (1 + L)
                    index = np.where(np.isfinite(index), index, 0)  # Replace NaN or Inf with 0
            else:
                # Handle other normalized difference calculations
                with np.errstate(divide="ignore", invalid="ignore"):
                    index = (numerator - denominator) / (numerator + denominator)
                    index = np.where(np.isfinite(index), index, 0)  # Replace NaN or Inf with 0

            # Standardize the values based on the index type
            index_ranges = {
                "NDVI": (-1, 1),  # NDVI range
                "NDWI": (-1, 1),  # NDWI range
                "NDBI": (-1, 1),  # NDBI range
                "SAVI": (-1, 1),  # SAVI range (adjustable with L)
            }

            if index_type in index_ranges:
                min_val, max_val = index_ranges[index_type]
                index = np.clip(index, min_val, max_val)  # Clip values to the specified range
            else:
                print(f"Warning: No standardization range defined for index type {index_type}. Skipping clipping.")

            return index
        except Exception as e:
            print(f"Error calculating {index_type}: {e}")
            raise
            
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
        try:
            print(f"Reprojecting scene: {scene_id} to {target_crs}...")

            # Get files associated with the scene
            scene_files = self.group_files_by_scene().get(scene_id, [])
            if not scene_files:
                print(f"No files found for scene {scene_id}. Skipping...")
                return

            for file_path in scene_files:
                # Skip non-raster files
                if not file_path.lower().endswith(('.tif', '.geotiff')):
                    continue

                try:
                    # Open the raster file
                    with rasterio.open(file_path) as src:
                        print(f"Processing file: {file_path}")

                        # Calculate the transform and metadata for the target CRS
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

                        # Create the output file path with "_reprojected" suffix
                        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
                        output_file = os.path.join(output_folder, f"{file_name}_reprojected{file_extension}")
                        os.makedirs(os.path.dirname(output_file), exist_ok=True)

                        # Perform reprojection
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

                        print(f"File reprojected and saved to: {output_file}")

                except rasterio.errors.RasterioIOError as rio_err:
                    print(f"RasterioIOError for file {file_path}: {rio_err}")
                except Exception as e:
                    print(f"Error reprojecting file {file_path}: {e}")

            print(f"Reprojection complete for scene: {scene_id}.")

        except Exception as e:
            print(f"Unexpected error while reprojecting scene {scene_id}: {e}")