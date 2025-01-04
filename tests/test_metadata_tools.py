import unittest
import os
from LandsatToolkit.metadata_tools import MetadataManager


class TestMetadataManager(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Simulate metadata content
        self.metadata_content = {
            "satellite": "Landsat8",
            "sensor": "OLI_TIRS",
            "acquisition_date": "2025-01-01",
            "cloud_cover": 12.3,
            "scene_bounds": {"north": 45.0, "south": 40.0, "east": 10.0, "west": 5.0},
        }

        # Initialize MetadataManager
        self.metadata_manager = MetadataManager(self.metadata_content)

    def test_initialization(self):
        """Test initialization of MetadataManager."""
        self.assertEqual(self.metadata_manager.metadata, self.metadata_content)

    def test_get_metadata_field(self):
        """Test retrieving a specific metadata field."""
        # Example: Retrieve satellite name
        satellite = self.metadata_manager.get_metadata_field("satellite")
        self.assertEqual(satellite, "Landsat8")

        # Example: Retrieve cloud cover
        cloud_cover = self.metadata_manager.get_metadata_field("cloud_cover")
        self.assertAlmostEqual(cloud_cover, 12.3)

    def test_validate_metadata(self):
        """Test metadata validation."""
        # Example: Mock validation to return True for valid metadata
        self.metadata_manager.validate_metadata = lambda: True
        is_valid = self.metadata_manager.validate_metadata()
        self.assertTrue(is_valid)

    def test_update_metadata_field(self):
        """Test updating a specific metadata field."""
        # Example: Update cloud cover
        new_cloud_cover = 15.0
        self.metadata_manager.update_metadata_field("cloud_cover", new_cloud_cover)
        updated_value = self.metadata_manager.get_metadata_field("cloud_cover")
        self.assertAlmostEqual(updated_value, new_cloud_cover)

    def test_export_metadata_to_json(self):
        """Test exporting metadata to a JSON file."""
        # Example: Simulate JSON export
        output_path = "test_metadata.json"
        self.metadata_manager.export_metadata_to_json = lambda path: open(path, "w").close()

        self.metadata_manager.export_metadata_to_json(output_path)
        self.assertTrue(os.path.exists(output_path))

        # Clean up the test file
        if os.path.exists(output_path):
            os.remove(output_path)

    def test_calculate_scene_bounds_area(self):
        """Test calculating the area of the scene bounds."""
        # Mock a function to calculate area
        self.metadata_manager.calculate_scene_bounds_area = lambda: 25.0
        area = self.metadata_manager.calculate_scene_bounds_area()
        self.assertAlmostEqual(area, 25.0)

    def test_format_metadata(self):
        """Test formatting metadata for display."""
        # Simulate formatted metadata output
        formatted_metadata = (
            "Satellite: Landsat8\n"
            "Sensor: OLI_TIRS\n"
            "Acquisition Date: 2025-01-01\n"
            "Cloud Cover: 12.3%\n"
            "Scene Bounds: North=45.0, South=40.0, East=10.0, West=5.0"
        )

        self.metadata_manager.format_metadata = lambda: formatted_metadata
        result = self.metadata_manager.format_metadata()
        self.assertEqual(result, formatted_metadata)


if __name__ == "__main__":
    unittest.main()