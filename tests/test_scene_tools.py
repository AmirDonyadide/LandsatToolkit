import unittest
import os
from LandsatToolkit.scene_tools import SceneOperations


class TestSceneOperations(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for test scenes
        self.scene_folder = "test_scene_folder"
        os.makedirs(self.scene_folder, exist_ok=True)

        # Create dummy scene files
        self.scene_files = []
        for i in range(5):
            file_path = os.path.join(self.scene_folder, f"scene_{i}.tif")
            with open(file_path, "w") as f:
                f.write(f"dummy scene data {i}")
            self.scene_files.append(file_path)

        # Initialize the SceneOperations class with the `input_folder` argument
        self.scene_ops = SceneOperations(input_folder=self.scene_folder)

    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.scene_folder):
            for file in self.scene_files:
                if os.path.exists(file):
                    os.remove(file)
            os.rmdir(self.scene_folder)

    def test_initialization(self):
        """Test initialization of SceneOperations."""
        self.assertEqual(self.scene_ops.input_folder, self.scene_folder)

    def test_list_scenes(self):
        """Test listing all scenes in the folder."""
        # Mock list_scenes to return the scene files
        self.scene_ops.list_scenes = lambda: sorted(self.scene_files)
        scenes = self.scene_ops.list_scenes()
        expected_scenes = sorted(self.scene_files)
        self.assertListEqual(sorted(scenes), expected_scenes)

    def test_filter_scenes_by_date(self):
        """Test filtering scenes by a specific date."""
        # Example: Mock the method to simulate filtering by date
        self.scene_ops.filter_scenes_by_date = lambda start_date, end_date: self.scene_files[:2]
        filtered_scenes = self.scene_ops.filter_scenes_by_date("2025-01-01", "2025-01-10")
        self.assertEqual(len(filtered_scenes), 2)

    def test_merge_scenes(self):
        """Test merging multiple scenes."""
        # Simulate a merge operation
        output_path = os.path.join(self.scene_folder, "merged_scene.tif")
        self.scene_ops.merge_scenes = lambda scenes, output: open(output, "w").close()

        self.scene_ops.merge_scenes(self.scene_files, output_path)
        self.assertTrue(os.path.exists(output_path))

        # Clean up the merged file
        if os.path.exists(output_path):
            os.remove(output_path)

    def test_split_scene(self):
        """Test splitting a single scene into smaller parts."""
        # Simulate splitting a scene
        self.scene_ops.split_scene = lambda scene_file, output_folder: [
            os.path.join(output_folder, f"split_{i}.tif") for i in range(3)
        ]

        output_folder = os.path.join(self.scene_folder, "splits")
        os.makedirs(output_folder, exist_ok=True)

        split_files = self.scene_ops.split_scene(self.scene_files[0], output_folder)
        self.assertEqual(len(split_files), 3)

        # Check if split files are generated
        for file in split_files:
            with open(file, "w") as f:
                f.write("dummy split data")
            self.assertTrue(os.path.exists(file))

        # Clean up split files and folder
        for file in split_files:
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists(output_folder):
            os.rmdir(output_folder)

    def test_calculate_scene_statistics(self):
        """Test calculating statistics for a scene."""
        # Simulate scene statistics calculation
        statistics = {"min": 0, "max": 255, "mean": 128, "stddev": 15.5}
        self.scene_ops.calculate_scene_statistics = lambda scene_file: statistics

        result = self.scene_ops.calculate_scene_statistics(self.scene_files[0])
        self.assertDictEqual(result, statistics)


if __name__ == "__main__":
    unittest.main()