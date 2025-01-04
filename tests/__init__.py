import os
import sys

# Add the main project directory to the system path to ensure test files can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Optional: Import individual test modules to streamline running tests
from .test_data_processor import TestSatelliteDataProcessor
from .test_scene_tools import TestSceneOperations
from .test_metadata_tools import TestMetadataManager
from .test_utils import TestUtils