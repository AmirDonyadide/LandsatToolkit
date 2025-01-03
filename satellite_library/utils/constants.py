"""
Constants

This module contains constants used throughout the library.
"""

# Band mappings for supported satellite types
BAND_MAPPING = {
    "landsat7": {
        "red": 2,    # Band 3
        "green": 1,  # Band 2
        "nir": 3,    # Band 4
        "swir": 4,   # Band 5
    },
    "landsat8": {
        "red": 3,    # Band 4
        "green": 2,  # Band 3
        "nir": 4,    # Band 5
        "swir": 5,   # Band 6
    },
    "landsat9": {
        "red": 3,    # Band 4
        "green": 2,  # Band 3
        "nir": 4,    # Band 5
        "swir": 5,   # Band 6
    },
}

# Default CRS for reprojection (UTM Zone 33N as an example)
DEFAULT_CRS = "EPSG:32633"

# Soil Adjustment Factor for SAVI Index
SAVI_L = 0.5

# Log Levels
LOG_LEVELS = {
    "INFO": "[INFO]",
    "WARNING": "[WARNING]",
    "ERROR": "[ERROR]",
}

# Supported Indices
SUPPORTED_INDICES = ["NDVI", "NDWI", "SAVI", "NDBI"]