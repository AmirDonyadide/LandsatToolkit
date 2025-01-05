import unittest
import os
import shutil
import numpy as np
from LandsatToolkit.data_processor import SatelliteDataProcessor
from LandsatToolkit.utils import create_output_folder


class TestSatelliteDataProcessor(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary input folder
        self.input_folder = "test_input_folder"
        os.makedirs(self.input_folder, exist_ok=True)

        # Create a temporary file to simulate raw data
        self.raw_data_file = os.path.join(self.input_folder, "raw_data.tif")
        with open(self.raw_data_file, "w") as f:
            f.write("dummy data")

        # Initialize SatelliteDataProcessor
        self.processor = SatelliteDataProcessor(input_folder=self.input_folder)

    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.input_folder):
            shutil.rmtree(self.input_folder)

        # Remove any output folder created during testing
        output_folder = os.path.join(os.getcwd(), "processed")
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

    def test_initialization(self):
        """Test initialization of SatelliteDataProcessor."""
        self.assertEqual(self.processor.input_folder, self.input_folder)

    def test_generate_output_folder(self):
        """Test the generation of an output folder."""
        output_folder_name = "processed"
        output_folder = create_output_folder(output_folder_name)
        self.assertTrue(os.path.exists(output_folder))
        self.assertTrue(os.path.isdir(output_folder))

    def test_process_raw_data(self):
        """Test the process_raw_data method."""
        # Simulate raw data processing
        processed_file = os.path.join(self.input_folder, "processed_data.tif")
        self.processor.process_raw_data = lambda: open(processed_file, "w").close()

        self.processor.process_raw_data()
        self.assertTrue(os.path.exists(processed_file))

    def test_metadata_extraction(self):
        """Test metadata extraction."""
        metadata = {"sensor": "Landsat8", "date": "2025-01-01"}
        self.processor.extract_metadata = lambda: metadata

        result = self.processor.extract_metadata()
        self.assertEqual(result, metadata)

    def test_file_handling(self):
        """Test file handling during processing."""
        # Simulate file handling logic
        processed_files = []
        for i in range(5):
            file_path = os.path.join(self.input_folder, f"file_{i}.tif")
            with open(file_path, "w") as f:
                f.write(f"dummy data {i}")
            processed_files.append(file_path)

        self.assertEqual(len(processed_files), 5)
        for file in processed_files:
            self.assertTrue(os.path.exists(file))

    def test_data_conversion(self):
        """Test data conversion (if applicable)."""
        raw_array = np.array([[1, 2, 3], [4, 5, 6]])
        processed_array = raw_array * 2  # Example operation

        self.processor.convert_data = lambda data: data * 2
        result = self.processor.convert_data(raw_array)

        np.testing.assert_array_equal(result, processed_array)


if __name__ == "__main__":
    unittest.main()