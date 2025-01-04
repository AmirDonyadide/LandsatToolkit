import os

# Constants
"""
Stores all constant values used across the library.
"""

DEFAULT_CRS = "EPSG:4326"  # Default Coordinate Reference System
SUPPORTED_INDICES = ["NDVI", "NDBI", "NDWI", "SAVI"]  # List of supported indices
DEFAULT_RESAMPLING_METHOD = "nearest"  # Default resampling method for reprojection


# Helper Functions
"""
Provides utility functions used across the library.
"""

def create_output_folder(base_folder_name):
    """
    Creates an output folder with a timestamp in its name.

    Args:
        base_folder_name (str): Base name of the folder to create.

    Returns:
        str: Path to the created folder.
    """
    try:
        folder_name = f"{base_folder_name}"
        folder_path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Output folder created: {folder_path}")
        return folder_path
    except PermissionError:
        print(f"Permission denied while creating folder: {folder_name}")
        raise
    except Exception as e:
        print(f"Error creating output folder '{base_folder_name}': {e}")
        raise

def validate_file_extension(file_name, valid_extensions):
    """
    Validates if a file has a valid extension.

    Args:
        file_name (str): Name of the file to validate.
        valid_extensions (list): List of valid extensions (e.g., ['.tif', '.geotiff']).

    Returns:
        bool: True if the file has a valid extension, False otherwise.
    """
    try:
        is_valid = any(file_name.lower().endswith(ext) for ext in valid_extensions)
        if not is_valid:
            print(f"Invalid file extension for file: {file_name}")
        return is_valid
    except Exception as e:
        print(f"Error validating file extension for '{file_name}': {e}")
        raise

def format_scene_list(scene_list):
    """
    Formats a list of scenes for display.

    Args:
        scene_list (list): List of scene IDs.

    Returns:
        str: Formatted string representation of the scene list.
    """
    try:
        if not scene_list:
            return "No scenes available."
        formatted_list = "\n".join(f"- {scene}" for scene in scene_list)
        return formatted_list
    except Exception as e:
        print(f"Error formatting scene list: {e}")
        raise