import unittest
import os
import shutil
from LandsatToolkit.utils import create_output_folder


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary folder
        self.temp_folder = "test_temp_folder"
        os.makedirs(self.temp_folder, exist_ok=True)

        # Change the current working directory to the temporary folder
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_folder)

    def tearDown(self):
        """Clean up the test environment."""
        # Change back to the original working directory
        os.chdir(self.original_cwd)

        # Remove the temporary folder
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

    def test_create_output_folder(self):
        """Test the create_output_folder utility function."""
        output_folder = "output"
        created_folder = create_output_folder(output_folder)
        self.assertTrue(os.path.exists(created_folder))
        self.assertEqual(created_folder, os.path.abspath(output_folder))

    def test_create_output_folder_already_exists(self):
        """Test create_output_folder when the folder already exists."""
        existing_folder = "existing_output"
        os.makedirs(existing_folder, exist_ok=True)

        created_folder = create_output_folder(existing_folder)
        self.assertTrue(os.path.exists(created_folder))
        self.assertEqual(created_folder, os.path.abspath(existing_folder))


if __name__ == "__main__":
    unittest.main()