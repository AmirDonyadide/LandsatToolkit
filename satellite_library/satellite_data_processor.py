import os
import datetime
from .scene_processor import SceneProcessor
from .metadata_manager import MetadataManager
from .index_calculator import IndexCalculator

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
        self.scene_processor = SceneProcessor(input_folder)
        self.metadata_manager = MetadataManager()
        self.index_calculator = IndexCalculator()

    def organize_data(self, output_folder=None):
        """
        Organize satellite data into the specified output folder.

        Args:
            output_folder (str): Path to the output folder for organized data.
        """
        # Handle default output folder
        if output_folder is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = os.path.join(os.getcwd(), f"output_organized_{timestamp}")
            os.makedirs(output_folder, exist_ok=True)
            print(f"No output folder specified. Using default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)
        
        print(f"Organizing satellite data into: {output_folder}")
        self.scene_processor.organize_satellite_data(output_folder)
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
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = os.path.join(os.getcwd(), f"output_indice_{timestamp}")
            os.makedirs(output_folder, exist_ok=True)
            print(f"No output folder specified. Using default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)

        # Handle default indices
        if indices is None:
            indices = ["NDVI", "NDBI", "NDWI", "SAVI"]  # All supported indices
            print("No indices specified. Calculating all supported indices.")
        elif isinstance(indices, str):
            indices = [indices]  # Convert a single string to a list

        # Group files by scene
        all_scenes = self.scene_processor.group_files_by_scene()

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

            try:
                # Create band matrix for the scene
                matrix = self.scene_processor.create_band_matrices(scene)
                for B4_finder in all_scenes[scene][:]:
                    if "_SR_B4" in B4_finder:
                        B4= B4_finder
                        break

                # Detect satellite type
                satellite_type = self.scene_processor.detect_satellite_type(B4)

                # Calculate indices and save results
                for index in indices:
                    scene_output_folder = os.path.join(output_folder, scene)
                    os.makedirs(scene_output_folder, exist_ok=True)
                    output_file = os.path.join(scene_output_folder, f"{index}.tif")
                    
                    self.index_calculator.calculate_and_save_index(
                        matrix, index, satellite_type, output_file, B4
                    )
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
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = os.path.join(os.getcwd(), f"output_metadata_{timestamp}")
            os.makedirs(output_folder, exist_ok=True)
            print(f"No output folder specified. Using default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)

        # Group files by scene
        all_scenes = self.scene_processor.group_files_by_scene()

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

            # Default output folder to `output/metadata/{scene_id}`
            scene_output_folder = output_folder if output_folder else os.path.join("output", "metadata", sid)
            os.makedirs(scene_output_folder, exist_ok=True)

            # Extract metadata using MetadataManager
            self.metadata_manager.extract_metadata(scene_output_folder, sid, self.input_folder)

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
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = os.path.join(os.getcwd(), f"output_reprojected_{timestamp}")
            os.makedirs(output_folder, exist_ok=True)
            print(f"No output folder specified. Using default: {output_folder}")
        else:
            os.makedirs(output_folder, exist_ok=True)

        # Group files by scene
        all_scenes = self.scene_processor.group_files_by_scene()

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
                self.scene_processor.reproject_scene(
                    scene_id=sid,
                    target_crs=target_crs,
                    output_folder=scene_output_folder
                )

                print(f"Reprojected scene {sid} files saved to {scene_output_folder}.")

            except Exception as e:
                print(f"Error reprojecting scene {sid}: {e}")

        print("Reprojection process complete.")