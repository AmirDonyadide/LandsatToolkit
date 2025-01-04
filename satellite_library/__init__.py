"""
Satellite Library
=================
A Python library for satellite data processing, including scene processing,
index calculation, metadata extraction, and utility functions.
"""

# Import key classes and modules for easy access
from .satellite_data_processor import SatelliteDataProcessor
from .scene_operations import SceneOperations
from .metadata_manager import MetadataManager
from .utils import DEFAULT_CRS, SUPPORTED_INDICES, create_output_folder, validate_file_extension


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