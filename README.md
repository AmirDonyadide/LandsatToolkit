# LandsatToolkit

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**LandsatToolkit** is a versatile Python library designed to simplify the processing and analysis of satellite imagery from **Landsat 7, 8, and 9**. With an intuitive interface and robust functionality, it enables users to efficiently handle metadata, process imagery, and execute advanced scene operations. Whether you’re working on Earth observation, environmental monitoring, or geospatial analysis, LandsatToolkit provides the tools you need to unlock insights from satellite data with ease.

---

## Features

- **Metadata Management**:
  - Extract metadata from Landsat imagery files.
  - Parse and manipulate metadata for easy integration into workflows.
- **Satellite Data Processing**:
  - Preprocess Landsat data, including calibration and rescaling.
  - Support for band extraction and composition.
- **Scene Operations**:
  - Perform calculations such as NDVI (Normalized Difference Vegetation Index).
  - Create band combinations for visualizations (e.g., True Color, False Color).
  - Apply scene-based adjustments like cloud masking.
- **Utility Functions**:
  - General-purpose helper functions to simplify file management, data formatting, and other repetitive tasks.
- **Compatibility**:
  - Works seamlessly with data from Landsat 7, 8, and 9.

---

## Installation

To install **LandsatToolkit**, follow these steps:

1. **Clone the Repository**:  
   Begin by cloning the repository from GitHub to your local machine.
   ```bash
   git clone https://github.com/AmirDonyadide/LandsatToolkit.git
   ```

2. **Activate the Appropriate Python Environment**:  
   Open your terminal and activate the Python environment where you want to install the library.
   ```bash
   conda activate your_environment_name
   ```

3. **Navigate to the Repository Folder**:  
   Change the directory to the folder where the repository is located.
   ```bash
   cd LandsatToolkit
   ```

4. **Install the Library**:  
   Use pip to install the library in editable mode.
   ```bash
   pip install -e .
   ```

After installation, you can import and use **LandsatToolkit** in your Python projects.

---

## Getting Started

### Importing the Library

Start by importing the required modules from the library:

```python
from LandsatToolkit.data_processor import SatelliteDataProcessor
```

### Example Usage

#### Initialize the processor
```python
data_folder = SatelliteDataProcessor(input_folder="path/to/Landsat/files")
```
 #### Explanation:
- `input_folder` *(str)*: The path to the folder containing raw Landsat data files.  
- The `SatelliteDataProcessor` instance is now ready to process raw data, extract metadata, and perform other operations on the provided data.


#### Extract Metadata

You can extract metadata from Landsat scenes using the `extract_metadata` method. The method allows flexibility with parameters like `output_folder` and `scene_id`.

```python
# Extract metadata for all scenes (output folder will be created automatically)
data_folder.extract_metadata()

# Extract metadata for a specific scene ID (output folder will be created automatically)
data_folder.extract_metadata(scene_id="LC08_L1TP_034032_20230712_20230723_02_T1")

# Extract metadata for multiple scene IDs with a custom output folder
scene_ids = ["LC08_L1TP_034032_20230712_20230723_02_T1", "LC08_L1TP_034033_20230712_20230723_02_T1"]
data_folder.extract_metadata(output_folder="custom_folder", scene_id=scene_ids)
```

##### Parameters:
- `output_folder` *(optional, str)*:  
  - Specifies the folder where extracted metadata will be saved.  
  - If not provided, a folder named `output_metadata_<timestamp>` will be created automatically in the current directory.
  
- `scene_id` *(optional, str or list of str)*:  
  - A single scene ID or a list of scene IDs to extract metadata for.  
  - If not provided, metadata for all scenes in the `data_folder` will be extracted.


#### Calculate Indices

You can calculate indices from Landsat scenes using the `indice_calculator` method. The method allows flexibility with parameters like `output_folder` , `indices` and `scene_id`.

```python
# Extract indices for all scenes and all indices (output folder will be created automatically)
data_folder.indice_calculator()

# Extract indices for a specific scene ID and all indices (output folder will be created automatically)
data_folder.indice_calculator(scene_id="LC08_L1TP_034032_20230712_20230723_02_T1")

# Extract indice for multiple scene IDs with a custom output folder
scene_ids = ["LC08_L1TP_034032_20230712_20230723_02_T1", "LC08_L1TP_034033_20230712_20230723_02_T1"]
data_folder.extract_metadata(output_folder="custom_folder", indices="NDVI" ,scene_id=scene_ids)
```

##### Parameters:
- `output_folder` *(optional, str)*:  
  - Specifies the folder where extracted indices will be saved.  
  - If not provided, a folder named `output_indices_<timestamp>` will be created automatically in the current directory.

- `indices` *(optional, str or list of str)*:  
  - A single indice or a list of indices to extract indice for.  
  - If not provided, indices for all scenes in the `data_folder` will be extracted.
  
- `scene_id` *(optional, str or list of str)*:  
  - A single scene ID or a list of scene IDs to extract metadata for.  
  - If not provided, indices for all scenes in the `data_folder` will be extracted.


#### Organize Data

You can organize data from Landsat scenes using the `organize_data` method. The method allows flexibility with parameter like `output_folder` .

```python
# Organize files for all scenes (output folder will be created automatically)
data_folder.organize_data()

# Extract indices for a specific scene ID and all indices (output folder will be created automatically)
data_folder.organize_data(output_folder="custom_folder")
```

##### Parameters:
- `output_folder` *(optional, str)*:  
  - Specifies the folder where extracted indices will be saved.  
  - If not provided, a folder named `output_organized_<timestamp>` will be created automatically in the current directory.


#### Reproject Bands

You can reproject bands from Landsat scenes using the `reproject` method. The method allows flexibility with parameters like `output_folder` , `scene_id` and `target_crs`.

```python
# Reproject bands for all scenes (output folder will be created automatically)
data_folder.reproject(target_crs="EPSG:32633")

# Reproject bands for a specific scene ID (output folder will be created automatically)
data_folder.reproject(scene_id="LC08_L1TP_034032_20230712_20230723_02_T1",target_crs="EPSG:32633")

# Extract indice for multiple scene IDs with a custom output folder
scene_ids = ["LC08_L1TP_034032_20230712_20230723_02_T1", "LC08_L1TP_034033_20230712_20230723_02_T1"]
data_folder.reproject(scene_id="LC08_L1TP_034032_20230712_20230723_02_T1", scene_id=scene_id, target_crs="EPSG:32633")
```

##### Parameters:
- `output_folder` *(optional, str)*:  
  - Specifies the folder where extracted indices will be saved.  
  - If not provided, a folder named `output_indices_<timestamp>` will be created automatically in the current directory.
  
- `scene_id` *(optional, str or list of str)*:  
  - A single scene ID or a list of scene IDs to extract metadata for.  
  - If not provided, indices for all scenes in the `data_folder` will be extracted.

- `target_crs` *(str)*:  
  - If not provided, appropriate error will be shown.
---


## Project Structure

Here’s an overview of the directory structure:

```
LandsatToolkit/
├── LandsatToolkit/
│   ├── __init__.py
│   ├── metadata_manager.py         # Functions for metadata extraction
│   ├── satellite_data_processor.py # Modules for Landsat image preprocessing
│   ├── scene_operations.py         # Scene-based operations like NDVI calculation
│   ├── utils.py                    # General utility functions
├── LICENSE                         # MIT License details
├── README.md                       # Project documentation
├── VERSION                         # Current version of the library
├── setup.py                        # Installation script
```

---

## Versioning

This project follows [Semantic Versioning](https://semver.org/).  
Current version: **1.1.2**

---

## Roadmap

Planned features and updates include:

- Adding support for Landsat 5 and earlier datasets.
- Incorporating machine learning models for cloud detection and land cover classification.
- Expanding scene operations to include more vegetation and water indices.
- Developing an interactive visualization module for Landsat data.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request detailing your changes.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## Contact

If you have any questions or need support, feel free to reach out:

- **GitHub Issues**: Open an issue in the repository.
- **Email**: [your-email@example.com] (Replace with your email address if you want to include it.)

---
