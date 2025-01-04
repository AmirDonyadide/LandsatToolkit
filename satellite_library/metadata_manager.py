import os

class MetadataManager:
    """
    Handles metadata extraction and parsing for satellite data.
    """

    def extract_metadata(self, output_folder, scene_id, input_folder):
        """
        Extract metadata for a specific scene and save to the output folder.

        Args:
            output_folder (str): Path to the folder where metadata should be saved.
            scene_id (str): Scene ID to extract metadata for.
            input_folder (str): Path to the folder containing satellite image files.

        Returns:
            None
        """
        try:
            # Group files by scene
            scenes = self._group_files_by_scene(input_folder)

            if scene_id not in scenes:
                print(f"Scene '{scene_id}' not found in input folder. Skipping...")
                return

            files = scenes[scene_id]
            metadata_file = next((f for f in files if f.lower().endswith("_mtl.txt")), None)
            if not metadata_file:
                print(f"No metadata file found for scene '{scene_id}'. Skipping...")
                return

            # Parse metadata
            metadata = self._parse_metadata(metadata_file)

            # Ensure the output folder exists
            os.makedirs(output_folder, exist_ok=True)

            # Save metadata to a tabular text file
            output_file_path = os.path.join(output_folder, f"{scene_id}_metadata.txt")
            self._save_metadata(metadata, output_file_path)
            print(f"Metadata for scene '{scene_id}' saved to {output_file_path}.")

        except Exception as e:
            print(f"Error extracting metadata for scene '{scene_id}': {e}")

    def _group_files_by_scene(self, folder_path):
        """
        Groups files by scene based on naming conventions.

        Args:
            folder_path (str): Path to the folder containing files.

        Returns:
            dict: A dictionary where keys are scene IDs and values are lists of file paths.
        """
        try:
            scenes = {}
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"Input folder '{folder_path}' does not exist.")

            for file_name in os.listdir(folder_path):
                if file_name.startswith(".") or not file_name.endswith(".txt"):
                    continue

                scene_id = "_".join(file_name.split("_")[:7])
                scenes.setdefault(scene_id, []).append(os.path.join(folder_path, file_name))
            return scenes

        except Exception as e:
            print(f"Error grouping files by scene: {e}")
            return {}

    def _parse_metadata(self, metadata_file_path):
        """
        Parses the metadata file and extracts key-value pairs.

        Args:
            metadata_file_path (str): Path to the metadata file.

        Returns:
            dict: Parsed metadata as a nested dictionary.
        """
        metadata = {}
        current_group = None
        try:
            with open(metadata_file_path, "r") as file:
                for line in file:
                    line = line.strip()

                    if line.startswith("GROUP ="):
                        current_group = line.split("GROUP =")[1].strip()
                        metadata[current_group] = {}
                    elif line.startswith("END_GROUP"):
                        current_group = None
                    elif "=" in line and current_group:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"')  # Remove quotes
                        metadata[current_group][key] = value
            return metadata

        except FileNotFoundError:
            print(f"Metadata file '{metadata_file_path}' not found.")
        except Exception as e:
            print(f"Error parsing metadata file '{metadata_file_path}': {e}")
        return metadata

    def _save_metadata(self, metadata, output_file_path):
        """
        Saves parsed metadata to a tabular text file.

        Args:
            metadata (dict): Metadata to save.
            output_file_path (str): Path to the output file.

        Returns:
            None
        """
        try:
            with open(output_file_path, "w") as file:
                for group, values in metadata.items():
                    file.write(f"### {group}\n")
                    file.write(f"{'Key':<40} {'Value':<60}\n")
                    file.write(f"{'-' * 100}\n")
                    for key, value in values.items():
                        file.write(f"{key:<40} {value:<60}\n")
                    file.write("\n")
        except PermissionError:
            print(f"Permission denied while writing to file '{output_file_path}'.")
        except Exception as e:
            print(f"Error saving metadata to file '{output_file_path}': {e}")