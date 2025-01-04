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