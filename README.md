# Satellite Library

A Python library for processing and analyzing satellite data. This library provides tools for organizing, reprojecting, creating band matrices, calculating indices (e.g., NDVI, NDWI, SAVI), and extracting metadata from satellite imagery.

---

## Features
- Organize satellite data by scenes and satellite types.
- Reproject raster files to a specified coordinate reference system (CRS).
- Calculate popular remote sensing indices like NDVI, NDWI, SAVI, and more.
- Parse and export metadata from satellite files.
- Supports Landsat 7, Landsat 8, and Landsat 9 satellite data.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/satellite-library.git
   cd satellite-library

	2.	Install via pip:

pip install .


	3.	Install Development Dependencies (optional):

pip install .[dev]

Quick Start

1. Organize Satellite Data

Organize raw satellite files into directories by scene and satellite type.

from satellite_library.satellite_data_processor import SatelliteDataProcessor

processor = SatelliteDataProcessor(input_folder="data/raw", output_folder="data/organized")
processor.organize_data()

2. Reproject and Process Scenes

Reproject raster files, create band matrices, and calculate indices like NDVI.

processor.process_all_scenes(target_crs="EPSG:32633", indices=["NDVI", "NDWI"])

3. Extract Metadata

Parse and save metadata for all scenes.

processor.extract_metadata()

Example Code

A complete example of processing satellite data:

from satellite_library.satellite_data_processor import SatelliteDataProcessor

# Initialize the processor
processor = SatelliteDataProcessor(
    input_folder="data/raw",
    output_folder="data/processed"
)

# Organize files
processor.organize_data()

# Reproject and calculate NDVI and NDWI
processor.process_all_scenes(target_crs="EPSG:32633", indices=["NDVI", "NDWI"])

# Extract metadata
processor.extract_metadata()

Supported Indices
	•	NDVI: Normalized Difference Vegetation Index
	•	NDWI: Normalized Difference Water Index
	•	SAVI: Soil-Adjusted Vegetation Index
	•	NDBI: Normalized Difference Built-Up Index
	•	EVI: Enhanced Vegetation Index
	•	MNDWI: Modified Normalized Difference Water Index

File Structure

Your folder structure might look like this:

SATELLITE_LIBRARY/
├── satellite_library/
│   ├── __init__.py
│   ├── index_calculator.py
│   ├── metadata_manager.py
│   ├── satellite_data_processor.py
│   ├── scene_processor.py
│   └── utils/
│       ├── __init__.py
│       ├── constants.py
│       └── helper_functions.py
├── examples/
│   ├── process_scene.py
│   └── calculate_indices.py
├── tests/
│   ├── test_index_calculator.py
│   ├── test_metadata_manager.py
│   ├── test_scene_processor.py
├── LICENSE
├── README.md
├── setup.py
└── VERSION

Contributing

We welcome contributions! To contribute:
	1.	Fork the repository.
	2.	Create a feature branch (git checkout -b feature-name).
	3.	Commit your changes (git commit -m "Add feature name").
	4.	Push to the branch (git push origin feature-name).
	5.	Create a pull request.

License

This library is licensed under the MIT License. See the LICENSE file for details.

Contact

For questions, issues, or feature requests:
	•	Author One: author1@example.com
	•	Author Two: author2@example.com
	•	GitHub Issues: Open an Issue
