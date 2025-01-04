import os
import rasterio
import numpy as np
import datetime
from .scene_operations import SceneOperations  # Use SceneOperations directly
from .metadata_manager import MetadataManager
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
        self.input_folder = input_folder
        self.scene_operations = SceneOperations(input_folder)
        self.metadata_manager = MetadataManager()

    def organize_data(self, output_folder=None):
        """
        Organize satellite data into the specified output folder.

        Args:
            output_folder (str): Path to the output folder for organized data.
        """
        # Handle default output folder
        if output_folder is None:
            path="output_organized_"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            output_folder = create_output_folder(path)
            print(f"No output folder specified.\nUsing default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)
        
        print(f"Organizing satellite data into: {output_folder}")
        self.scene_operations.organize_satellite_data(output_folder)
        print("Data organization complete.")

    def indice_calculator(self, output_folder=None, indices=None, scene_id=None):
        """
        Calculate indices for specific scenes and save to the specified output folder.

        Args:
            output_folder (str): Path where results will be saved. If None, creates a folder
                                named 'output_<code_run_time>' in the current working directory.
            indices (str or list of str): Indices to calculate. If None, all supported indices
                                        will be calculated.
            scene_id (str or list of str): Scene ID(s) to process. If None, all scenes in
                                        the input folder will be processed.
        """
        # Handle default output folder
        if output_folder is None:
            path="output_indices_"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            output_folder = create_output_folder(path)
            print(f"No output folder specified.\nUsing default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)

        # Handle default indices
        if indices is None:
            indices = ["NDVI", "NDBI", "NDWI", "SAVI"]  # All supported indices
            print("No indices specified. Calculating all supported indices.")
        elif isinstance(indices, str):
            indices = [indices]  # Convert a single string to a list

        # Group files by scene
        all_scenes = self.scene_operations.group_files_by_scene()

        # Handle default scenes
        if scene_id is None:
            scene_id = list(all_scenes.keys())  # Process all scenes
            print("No scene ID specified. Processing all scenes.")
        elif isinstance(scene_id, str):
            scene_id = [scene_id]  # Convert a single string to a list

        # Process each scene
        for scene in scene_id:
            if scene not in all_scenes:
                print(f"Scene ID '{scene}' not found in input folder. Skipping...")
                continue

            print(f"Processing scene: {scene}")

            try:
                # Create band matrix for the scene
                matrix = self.scene_operations.create_band_matrices(scene)

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
                satellite_type = self.scene_operations.detect_satellite_type(B4)

                # Calculate indices and save results
                for index in indices:
                    scene_output_folder = os.path.join(output_folder, scene)
                    os.makedirs(scene_output_folder, exist_ok=True)
                    output_file = os.path.join(scene_output_folder, f"{index}.tif")
                    
                    self.scene_operations.calculate_and_save_index(matrix, index, satellite_type, output_file,B4)

                    print(f"Saved {index} for scene {scene} to {output_file}")

            except Exception as e:
                print(f"Error processing scene {scene}: {e}")

        print("Index calculation complete.")
    
    def extract_metadata(self, output_folder=None, scene_id=None):
        """
        Extract metadata for one or more scenes and save to the specified output folder.

        Args:
            output_folder (str, optional): Path to the folder where metadata should be saved.
                                            Defaults to `output/metadata/{scene_id}` if not provided.
            scene_id (str or list of str, optional): Scene ID(s) to extract metadata for.
                                                    If not provided, all scenes in the input folder will be processed.
        """
        # Handle default output folder
        if output_folder is None:
            path="output_metadata_"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            output_folder = create_output_folder(path)
            print(f"No output folder specified.\nUsing default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)

        # Group files by scene
        all_scenes = self.scene_operations.group_files_by_scene()  # Updated to use SceneOperations

        # Handle default scenes
        if scene_id is None:
            scene_id = list(all_scenes.keys())  # Process all scenes
            print("No scene ID specified. Processing all scenes.")
        elif isinstance(scene_id, str):
            scene_id = [scene_id]  # Convert a single string to a list

        for sid in scene_id:
            if sid not in all_scenes:
                print(f"Scene ID '{sid}' not found in input folder. Skipping...")
                continue

            # Define scene-specific output folder
            scene_output_folder = os.path.join(output_folder, sid)
            os.makedirs(scene_output_folder, exist_ok=True)

            # Extract metadata using MetadataManager
            try:
                self.metadata_manager.extract_metadata(scene_output_folder, sid, self.input_folder)
                print(f"Metadata extracted and saved for scene: {sid}")
            except Exception as e:
                print(f"Error extracting metadata for scene '{sid}': {e}")
     
    def reproject(self, output_folder=None, scene_id=None, target_crs=None):
        """
        Reprojects raster files in the specified scene(s) to the target CRS.

        Args:
            output_folder (str, optional): Path to the folder where reprojected files should be saved.
                                        Defaults to `output_reprojected_<timestamp>` if not provided.
            scene_id (str or list of str, optional): Scene ID(s) to reproject. If None, all scenes in the input folder
                                                    will be reprojected.
            target_crs (str): Target CRS (e.g., "EPSG:32633").
        """
        # Ensure target CRS is provided
        if target_crs is None:
            raise ValueError("A target CRS must be specified (e.g., 'EPSG:32633').")

        # Handle default output folder
        if output_folder is None:
            path="output_reprojected_"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            output_folder = create_output_folder(path)
            print(f"No output folder specified.\nUsing default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)

        # Group files by scene
        all_scenes = self.scene_operations.group_files_by_scene()  # Updated to use SceneOperations

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
                # Create a folder for the reprojected files for the current scene
                scene_output_folder = os.path.join(output_folder, sid)
                os.makedirs(scene_output_folder, exist_ok=True)

                # Reproject all raster files for the scene
                self.scene_operations.reproject_scene(
                    scene_id=sid,
                    target_crs=target_crs,
                    output_folder=scene_output_folder
                )

                print(f"Reprojected scene {sid} files saved to {scene_output_folder}.")

            except Exception as e:
                print(f"Error reprojecting scene {sid}: {e}")

        print("Reprojection process complete.")
        
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
        # Handle default output folder
        if output_folder is None:
            path="output_merged_"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            output_folder = create_output_folder(path)
            print(f"No output folder specified.\nUsing default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)

        # Group files by scene
        all_scenes = self.scene_operations.group_files_by_scene()  # Updated to use SceneOperations

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
                    with rasterio.open(file_path) as src:
                        if meta is None:
                            meta = src.meta.copy()
                            meta.update(count=len(raster_files))  # Update meta for multi-band raster

                        band_data.append(src.read(1))  # Read the first band

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

    def show_scenes(self):
        """
        Display the list of scenes available in the processor.

        Returns:
            None
        """
        print("Retrieving list of scenes...")

        # Use SceneOperations to group files by scene
        all_scenes = self.scene_operations.group_files_by_scene()  # Updated to use SceneOperations

        # Check if there are any scenes
        if not all_scenes:
            print("No scenes found in the input folder.")
            return

        # Display the list of scenes
        print("Available Scenes:")
        for scene_id in sorted(all_scenes.keys()):
            print(f" - {scene_id}")

        print(f"\nTotal scenes: {len(all_scenes)}")