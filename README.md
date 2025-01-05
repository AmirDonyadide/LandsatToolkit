# LandsatToolkit

**LandsatToolkit** is a versatile Python library designed to simplify the processing and analysis of satellite imagery from **Landsat 7, 8, and 9**. With an intuitive interface and robust functionality, it enables users to efficiently handle metadata, process imagery, and execute advanced scene operations. Whether you’re working on Earth observation, environmental monitoring, or geospatial analysis, LandsatToolkit provides the tools you need to unlock insights from satellite data with ease.

---

## Features

- **Metadata Management**:
  - Extract metadata from Landsat imagery files.
- **Satellite Data Processing**:
  - Support for band composition.
- **Scene Operations**:
  - Perform calculations such as NDVI (Normalized Difference Vegetation Index).
- **Compatibility**:
  - Works seamlessly with data from Landsat 7, 8, and 9.

---

## Requirements

Make sure the following libraries are installed in your Python environment:
- numpy
- rasterio
-	shutil
- datetime
- os

---

## Installation

To install **LandsatToolkit**, follow these steps:

### **Online method**

1. **Install via pip**:
     
   ```bash
   pip install LandsatToolkit
   ```
### **Offline method**

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

# Reproject bands for multiple scene IDs with a custom output folder
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


#### Merge Bands

You can merge bands from Landsat scenes using the `merge_bands` method. The method allows flexibility with parameters like `output_folder` , `scene_id` and `bands`.

```python
# Merge bands for all scenes and all bands (output folder will be created automatically)
data_folder.merge_bands()

# Merge bands for a specific scene ID and all bands (output folder will be created automatically)
data_folder.merge_bands(scene_id="LC08_L1TP_034032_20230712_20230723_02_T1")

# Merge specific bands for all scenes(output folder will be created automatically)
data_folder.merge_bands(bands=["B1", "B2", "B3"])

# Merge bands for multiple scene IDs with a custom output folder and specific bands
scene_ids = ["LC08_L1TP_034032_20230712_20230723_02_T1", "LC08_L1TP_034033_20230712_20230723_02_T1"]
data_folder.merge_bands(scene_id="LC08_L1TP_034032_20230712_20230723_02_T1", scene_id=scene_id, bands=["B1", "B2", "B3"])
```

##### Parameters:
- `output_folder` *(optional, str)*:  
  - Specifies the folder where extracted indices will be saved.  
  - If not provided, a folder named `output_indices_<timestamp>` will be created automatically in the current directory.
  
- `scene_id` *(optional, str or list of str)*:  
  - A single scene ID or a list of scene IDs to extract metadata for.  
  - If not provided, indices for all scenes in the `data_folder` will be extracted.

- `bands` *(optional, str or list of str)*: 
  - If not provided, all bands will be considered.

---

## Project Structure

Here’s an overview of the directory structure:

```
LandsatToolkit/
├── LandsatToolkit/
│   ├── __init__.py
│   ├── data_processor.py           # Modules for Landsat image preprocessing
│   ├── metadata_tools.py           # Functions for metadata extraction
│   ├── scene_tools.py              # Scene-based operations like NDVI calculation
│   ├── utils.py                    # General utility functions
├── tests/
│   ├── __init__.py
│   ├── test_data_processor.py
│   ├── test_metadata_tools.py
│   ├── test_scene_tools.py
│   ├── test_utils.py
├── LICENSE                         # MIT License details
├── README.md                       # Project documentation
├── VERSION                         # Current version of the library
├── setup.py                        # Installation script
```

---

## Versioning

Current version: **1.0.0**

---

## Roadmap

Planned features and updates include:

- Adding support for Sentinel 2 , Landsat 5 and earlier datasets.
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
- **Email**: [amirhossein.donyadidegan@mail.polimi.it]
- - **Email**: [mohammad.kordgholiabad@mail.polimi.it]

---
