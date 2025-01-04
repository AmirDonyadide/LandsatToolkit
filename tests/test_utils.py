import unittest
import os
import shutil
from LandsatToolkit.utils import create_output_folder, validate_file_path, calculate_ndvi


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary folder and files
        self.temp_folder = "test_temp_folder"
        os.makedirs(self.temp_folder, exist_ok=True)

        # Create a dummy file
        self.dummy_file = os.path.join(self.temp_folder, "dummy.txt")
        with open(self.dummy_file, "w") as f:
            f.write("dummy content")

    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

    def test_create_output_folder(self):
        """Test the create_output_folder utility function."""
        output_folder = os.path.join(self.temp_folder, "output")
        created_folder = create_output_folder(self.temp_folder, "output")
        self.assertTrue(os.path.exists(created_folder))
        self.assertEqual(created_folder, output_folder)

    def test_validate_file_path_valid(self):
        """Test validate_file_path with a valid file path."""
        is_valid = validate_file_path(self.dummy_file)
        self.assertTrue(is_valid)

    def test_validate_file_path_invalid(self):
        """Test validate_file_path with an invalid file path."""
        invalid_file = os.path.join(self.temp_folder, "nonexistent.txt")
        is_valid = validate_file_path(invalid_file)
        self.assertFalse(is_valid)

    def test_calculate_ndvi(self):
        """Test calculate_ndvi function."""
        import numpy as np

        # Simulated Red and NIR bands
        red_band = np.array([[0.2, 0.3, 0.4], [0.5, 0.6, 0.7]])
        nir_band = np.array([[0.8, 0.9, 1.0], [1.1, 1.2, 1.3]])

        # Expected NDVI calculation
        expected_ndvi = (nir_band - red_band) / (nir_band + red_band)

        # Calculate NDVI using the utility function
        ndvi = calculate_ndvi(nir_band, red_band)

        # Assert that the calculated NDVI matches the expected values
        np.testing.assert_array_almost_equal(ndvi, expected_ndvi)

    def test_create_output_folder_already_exists(self):
        """Test create_output_folder when the folder already exists."""
        existing_folder = os.path.join(self.temp_folder, "existing_output")
        os.makedirs(existing_folder, exist_ok=True)

        # Call the function and ensure no error occurs
        created_folder = create_output_folder(self.temp_folder, "existing_output")
        self.assertTrue(os.path.exists(created_folder))
        self.assertEqual(created_folder, existing_folder)

    def test_calculate_ndvi_edge_cases(self):
        """Test calculate_ndvi with edge cases (e.g., division by zero)."""
        import numpy as np

        # Simulated Red and NIR bands with zeroes
        red_band = np.array([[0.0, 0.3, 0.4], [0.5, 0.0, 0.7]])
        nir_band = np.array([[0.0, 0.9, 1.0], [1.1, 0.0, 1.3]])

        # Expected NDVI calculation (handle division by zero gracefully)
        expected_ndvi = np.divide(
            nir_band - red_band, nir_band + red_band, out=np.zeros_like(nir_band), where=(nir_band + red_band) != 0
        )

        # Calculate NDVI using the utility function
        ndvi = calculate_ndvi(nir_band, red_band)

        # Assert that the calculated NDVI matches the expected values
        np.testing.assert_array_almost_equal(ndvi, expected_ndvi)


if __name__ == "__main__":
    unittest.main()