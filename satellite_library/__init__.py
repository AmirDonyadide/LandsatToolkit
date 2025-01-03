"""
Satellite Library

This package provides tools for processing and analyzing satellite data, including:
- Organizing satellite data by scenes and satellite types.
- Reprojecting and creating band matrices.
- Calculating indices such as NDVI, NDWI, and SAVI.
- Extracting and parsing metadata.

Modules:
- satellite_data_processor: High-level manager for satellite data processing.
- scene_processor: Handles scene-specific operations.
- index_calculator: Calculates various indices from satellite data.
- metadata_manager: Extracts and parses metadata files.

Example usage:
    from satellite_library import SatelliteDataProcessor

    processor = SatelliteDataProcessor(input_folder="path/to/input", output_folder="path/to/output")
    processor.organize_data()
    processor.process_all_scenes(target_crs="EPSG:32633", indices=["NDVI", "NDWI"])
"""

from .satellite_data_processor import SatelliteDataProcessor
from .scene_processor import SceneProcessor
from .index_calculator import IndexCalculator
from .metadata_manager import MetadataManager