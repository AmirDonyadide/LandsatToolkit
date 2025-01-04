import os
import rasterio
import numpy as np
import datetime
from .scene_tools import SceneOperations
from .metadata_tools import MetadataManager
from .utils import create_output_folder

class SatelliteDataProcessor:
    """
    High-level manager for satellite data processing.
    """
    def __init__(self, input_folder):
        """
        Initialize the SatelliteDataProcessor with the input folder path.

        Args:
            input_folder (str): Path to the input folder containing raw satellite data.
        """
        if not os.path.exists(input_folder):
            raise ValueError(f"Input folder '{input_folder}' does not exist.")

        self.input_folder = input_folder

        # Initialize sub-components for processing
        try:
            self.scene_tools = SceneOperations(input_folder)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize SceneOperations: {e}")

        try:
            self.metadata_tools = MetadataManager()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize MetadataManager: {e}")

        print(f"SatelliteDataProcessor initialized with input folder: {input_folder}")
   
    def organize_data(self, output_folder=None):
        """
        Organize satellite data into the specified output folder.

        Args:
            output_folder (str, optional): Path to the output folder for organized data.
                                        If None, a default timestamped folder is created.

        Returns:
            None
        """
        try:
            # Handle default output folder
            if output_folder is None:
                path = "output_organized_" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
                output_folder = create_output_folder(path)
                print(f"No output folder specified.\nUsing default: {output_folder}")
            else:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder, exist_ok=True)
                    print(f"Created specified output folder: {output_folder}")
                else:
                    print(f"Using existing output folder: {output_folder}")
            
            print(f"Organizing satellite data into: {output_folder}")
            
            # Call the scene_tools method to organize the data
            self.scene_tools.organize_satellite_data(output_folder)
            print("Data organization complete.")
        
        except PermissionError as e:
            print(f"PermissionError: Unable to write to the specified output folder '{output_folder}'.\n{e}")
        except FileNotFoundError as e:
            print(f"FileNotFoundError: Input folder or files are missing.\n{e}")
        except Exception as e:
            print(f"An unexpected error occurred during data organization: {e}")

    def indice_calculator(self, output_folder=None, indices=None, scene_id=None, L=None):
        """
        Calculate indices for specific scenes and save to the specified output folder.

        Args:
            output_folder (str): Path where results will be saved. If None, creates a folder
                                named 'output_indices_<timestamp>' in the current working directory.
            indices (str or list of str): Indices to calculate. If None, all supported indices
                                        will be calculated.
            scene_id (str or list of str): Scene ID(s) to process. If None, all scenes in
                                        the input folder will be processed.
        """
        try:
            # Handle default output folder
            if output_folder is None:
                path = "output_indices_" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
                output_folder = create_output_folder(path)
                print(f"No output folder specified.\nUsing default: {output_folder}")
            else:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder, exist_ok=True)
                    print(f"Created specified output folder: {output_folder}")
                else:
                    print(f"Using existing output folder: {output_folder}")

            # Handle default indices
            if indices is None:
                indices = ["NDVI", "NDBI", "NDWI", "SAVI"]  # All supported indices
                print("No indices specified. Calculating all supported indices.")
            elif isinstance(indices, str):
                indices = [indices]  # Convert a single string to a list

            # Group files by scene
            all_scenes = self.scene_tools.group_files_by_scene()

            # Handle default scenes
            if scene_id is None:
                scene_id = list(all_scenes.keys())  # Process all scenes
                print("No scene ID specified. Processing all scenes.")
            elif isinstance(scene_id, str):
                scene_id = [scene_id]  # Convert a single string to a list

            if L is None:
                L = 0.5
                print(f"No L value for SAVI specified. Using default value: {L}")
            else:
                L = float(L)
                
            # Process each scene
            for scene in scene_id:
                if scene not in all_scenes:
                    print(f"Scene ID '{scene}' not found in input folder. Skipping...")
                    continue

                print(f"Processing scene: {scene}")

                try:
                    # Create band matrix for the scene
                    matrix = self.scene_tools.create_band_matrices(scene)

                    # Find the B4 file
                    B4 = None
                    for file in all_scenes[scene]:
                        if "_SR_B4" in file.upper():
                            B4 = file
                            break

                    # Check if B4 is found
                    if not B4:
                        print(f"B4 reference file not found for scene {scene}. Available files: {all_scenes[scene]}")
                        continue  # Skip to the next scene

                    # Detect satellite type
                    satellite_type = self.scene_tools.detect_satellite_type(B4)

                    # Calculate indices and save results
                    for index in indices:
                        scene_output_folder = os.path.join(output_folder, scene)
                        os.makedirs(scene_output_folder, exist_ok=True)
                        output_file = os.path.join(scene_output_folder, f"{index}.tif")

                        # Use the updated calculate_and_save_index method
                        self.scene_tools.calculate_and_save_index(
                            band_matrix=matrix,
                            index_type=index,
                            satellite_type=satellite_type,
                            output_file=output_file,
                            B4=B4,
                            L=L if index == "SAVI" else None  # Pass L only if the index is SAVI
                        )
                        print(f"Saved {index} for scene {scene} to {output_file}")

                except FileNotFoundError as e:
                    print(f"FileNotFoundError while processing scene {scene}: {e}")
                except ValueError as e:
                    print(f"ValueError while processing scene {scene}: {e}")
                except Exception as e:
                    print(f"Unexpected error while processing scene {scene}: {e}")

            print("Index calculation complete.")

        except PermissionError as e:
            print(f"PermissionError: Unable to write to the specified output folder '{output_folder}'.\n{e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def extract_metadata(self, output_folder=None, scene_id=None):
        """
        Extract metadata for one or more scenes and save to the specified output folder.

        Args:
            output_folder (str, optional): Path to the folder where metadata should be saved.
                                        Defaults to a timestamped folder if not provided.
            scene_id (str or list of str, optional): Scene ID(s) to extract metadata for.
                                                    If not provided, all scenes in the input folder will be processed.
        """
        try:
            # Handle default output folder
            if output_folder is None:
                path = "output_metadata_" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
                output_folder = create_output_folder(path)
                print(f"No output folder specified.\nUsing default: {output_folder}")
            else:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder, exist_ok=True)
                    print(f"Specified output folder created: {output_folder}")
                else:
                    print(f"Using existing output folder: {output_folder}")

            # Group files by scene
            try:
                all_scenes = self.scene_tools.group_files_by_scene()  # Use SceneOperations to group files
            except Exception as e:
                print(f"Error grouping files by scene: {e}")
                return

            # Handle default scenes
            if scene_id is None:
                scene_id = list(all_scenes.keys())  # Process all scenes
                print("No scene ID specified. Processing all scenes.")
            elif isinstance(scene_id, str):
                scene_id = [scene_id]  # Convert a single string to a list

            # Process each scene
            for sid in scene_id:
                if sid not in all_scenes:
                    print(f"Scene ID '{sid}' not found in input folder. Skipping...")
                    continue

                # Define scene-specific output folder
                scene_output_folder = os.path.join(output_folder, sid)
                os.makedirs(scene_output_folder, exist_ok=True)

                # Extract metadata using MetadataManager
                try:
                    print(f"Extracting metadata for scene: {sid}...")
                    self.metadata_tools.extract_metadata(scene_output_folder, sid, self.input_folder)
                    print(f"Metadata extracted and saved for scene: {sid}")
                except FileNotFoundError as e:
                    print(f"FileNotFoundError while extracting metadata for scene '{sid}': {e}")
                except PermissionError as e:
                    print(f"PermissionError: Unable to save metadata for scene '{sid}': {e}")
                except Exception as e:
                    print(f"Unexpected error while extracting metadata for scene '{sid}': {e}")

            print("Metadata extraction process complete.")

        except PermissionError as e:
            print(f"PermissionError: Unable to create or write to the specified output folder '{output_folder}'.\n{e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def reproject(self, output_folder=None, scene_id=None, target_crs=None):
        """
        Reprojects raster files in the specified scene(s) to the target CRS.

        Args:
            output_folder (str, optional): Path to the folder where reprojected files should be saved.
                                        Defaults to `output_reprojected_<timestamp>` if not provided.
            scene_id (str or list of str, optional): Scene ID(s) to reproject. If None, all scenes in the input folder
                                                    will be reprojected.
            target_crs (str): Target CRS (e.g., "EPSG:32633").

        Returns:
            None
        """
        try:
            # Ensure target CRS is provided
            if target_crs is None:
                raise ValueError("A target CRS must be specified (e.g., 'EPSG:32633').")

            # Handle default output folder
            if output_folder is None:
                path = "output_reprojected_" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
                output_folder = create_output_folder(path)
                print(f"No output folder specified.\nUsing default: {output_folder}")
            else:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder, exist_ok=True)
                    print(f"Specified output folder created: {output_folder}")
                else:
                    print(f"Using existing output folder: {output_folder}")

            # Group files by scene
            try:
                all_scenes = self.scene_tools.group_files_by_scene()
            except Exception as e:
                print(f"Error grouping files by scene: {e}")
                return

            # Handle default scenes
            if scene_id is None:
                scene_id = list(all_scenes.keys())  # Process all scenes
                print("No scene ID specified. Reprojecting all scenes.")
            elif isinstance(scene_id, str):
                scene_id = [scene_id]  # Convert a single string to a list

            # Process each scene
            for sid in scene_id:
                if sid not in all_scenes:
                    print(f"Scene ID '{sid}' not found in input folder. Skipping...")
                    continue

                try:
                    print(f"Reprojecting scene: {sid}...")
                    
                    # Create a folder for the reprojected files for the current scene
                    scene_output_folder = os.path.join(output_folder, sid)
                    os.makedirs(scene_output_folder, exist_ok=True)

                    # Reproject all raster files for the scene
                    self.scene_tools.reproject_scene(
                        scene_id=sid,
                        target_crs=target_crs,
                        output_folder=scene_output_folder
                    )

                    print(f"Reprojected files for scene {sid} saved to {scene_output_folder}.")

                except FileNotFoundError as e:
                    print(f"FileNotFoundError while reprojecting scene '{sid}': {e}")
                except PermissionError as e:
                    print(f"PermissionError: Unable to reproject files for scene '{sid}': {e}")
                except Exception as e:
                    print(f"Unexpected error while reprojecting scene '{sid}': {e}")

            print("Reprojection process complete.")

        except ValueError as e:
            print(f"ValueError: {e}")
        except PermissionError as e:
            print(f"PermissionError: Unable to create or write to the specified output folder '{output_folder}'.\n{e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
                    
    def merge_bands(self, output_folder=None, scene_id=None, bands=None):
        """
        Merge bands for one or more scenes into a single multi-band raster file.

        Args:
            output_folder (str, optional): Path to the folder where the merged raster files will be saved.
                                        Defaults to a generated folder if not specified.
            scene_id (str or list of str, optional): Scene ID(s) to process. If None, all scenes will be processed.
            bands (list of str, optional): List of band file suffixes to merge (e.g., ["_SR_B1", "_SR_B2"]).
                                        If None, all bands in the scene will be merged.

        Returns:
            None
        """
        try:
            # Handle default output folder
            if output_folder is None:
                path = "output_merged_" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
                output_folder = create_output_folder(path)
                print(f"No output folder specified.\nUsing default: {output_folder}")
            else:
                os.makedirs(output_folder, exist_ok=True)

            # Group files by scene
            try:
                all_scenes = self.scene_tools.group_files_by_scene()
            except Exception as e:
                print(f"Error grouping files by scene: {e}")
                return

            # Handle default scenes
            if scene_id is None:
                scene_id = list(all_scenes.keys())  # Process all scenes
                print("No scene ID specified. Processing all scenes.")
            elif isinstance(scene_id, str):
                scene_id = [scene_id]  # Convert a single string to a list

            # Process each scene
            for sid in scene_id:
                if sid not in all_scenes:
                    print(f"Scene ID '{sid}' not found in input folder. Skipping...")
                    continue

                print(f"Merging bands for scene: {sid}")

                # Filter bands if specified
                scene_files = all_scenes[sid]
                raster_files = [
                    f for f in scene_files if f.lower().endswith(('.tif', '.geotiff'))
                ]  # Include only raster files

                if bands:
                    filtered_files = []
                    for band in bands:
                        filtered_files.extend([f for f in raster_files if band in os.path.basename(f)])
                    raster_files = filtered_files

                if not raster_files:
                    print(f"No valid bands found for scene {sid}. Skipping...")
                    continue

                try:
                    # Read all bands and merge them
                    band_data = []
                    meta = None

                    for file_path in raster_files:
                        try:
                            with rasterio.open(file_path) as src:
                                if meta is None:
                                    meta = src.meta.copy()
                                    meta.update(count=len(raster_files))  # Update meta for multi-band raster

                                band_data.append(src.read(1))  # Read the first band
                        except rasterio.errors.RasterioIOError as e:
                            print(f"Error reading raster file {file_path}: {e}")
                            continue

                    if not band_data:
                        print(f"No valid data found in bands for scene {sid}. Skipping...")
                        continue

                    # Stack bands into a single array
                    merged_array = np.stack(band_data, axis=0)

                    # Create the output file
                    output_file = os.path.join(output_folder, f"{sid}_merged.tif")
                    with rasterio.open(output_file, "w", **meta) as dst:
                        for i in range(merged_array.shape[0]):
                            dst.write(merged_array[i], i + 1)

                    print(f"Merged raster saved to: {output_file}")

                except Exception as e:
                    print(f"Error merging bands for scene {sid}: {e}")

            print("Band merging process complete.")

        except Exception as e:
            print(f"An unexpected error occurred during band merging: {e}")
            
    def show_scenes(self):
        """
        Display the list of scenes available in the processor.

        Returns:
            None
        """
        print("Retrieving list of scenes...")

        try:
            # Use SceneOperations to group files by scene
            all_scenes = self.scene_tools.group_files_by_scene()

            # Check if there are any scenes
            if not all_scenes:
                print("No scenes found in the input folder.")
                return

            # Display the list of scenes
            print("Available Scenes:")
            for scene_id in sorted(all_scenes.keys()):
                print(f" - {scene_id}")

            print(f"\nTotal scenes: {len(all_scenes)}")

        except Exception as e:
            print(f"An error occurred while retrieving the list of scenes: {e}")