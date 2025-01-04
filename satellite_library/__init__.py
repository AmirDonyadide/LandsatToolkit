"""
Satellite Library
=================
A Python library for satellite data processing, including scene processing,
index calculation, metadata extraction, and utility functions.
"""

# Import key classes and modules for easy access
try:
    from .satellite_data_processor import SatelliteDataProcessor
    from .scene_operations import SceneOperations
    from .metadata_manager import MetadataManager
    from .utils import DEFAULT_CRS, SUPPORTED_INDICES, create_output_folder, validate_file_extension
except ImportError as e:
    print(f"Error importing modules in satellite_library: {e}")
    raise

# Expose key functionalities at the package level
__all__ = [
    "SatelliteDataProcessor",
    "SceneOperations",
    "MetadataManager",
    "DEFAULT_CRS",
    "SUPPORTED_INDICES",
    "create_output_folder",
    "validate_file_extension",
]

# Validate imports
def _validate_imports():
    """
    Validates all essential imports for the library.

    Returns:
        None
    """
    try:
        # Check if all required classes and functions are imported
        assert "SatelliteDataProcessor" in __all__
        assert "SceneOperations" in __all__
        assert "MetadataManager" in __all__
        assert "DEFAULT_CRS" in __all__
        assert "SUPPORTED_INDICES" in __all__
        print("All necessary modules and functions are successfully imported.")
    except AssertionError as e:
        print(f"Validation failed: {e}")
        raise ImportError("Critical modules or functions are missing in the package.")

# Run validation on module load
_validate_imports()