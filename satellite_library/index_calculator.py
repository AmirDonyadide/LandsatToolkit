import numpy as np
import rasterio

class IndexCalculator:
    """
    Calculates and saves various indices (e.g., NDVI, NDWI, SAVI) for satellite imagery.

    Example usage:
        calculator = IndexCalculator()
        calculator.calculate_and_save_index(matrix, "NDVI", "landsat8", "output_path.tif", "reference_file.tif")
    """

    def calculate_and_save_index(self, matrix, index_type, satellite_type, output_path, reference_file):
        """
        Calculates a specified index (e.g., NDVI, NDWI) from a multi-dimensional matrix
        and saves the result as a GeoTIFF file.

        Args:
            matrix (np.ndarray): 3D array where each dimension represents a band.
            index_type (str): The type of index to calculate (e.g., "NDVI", "NDWI", "SAVI").
            satellite_type (str): The type of satellite (e.g., "landsat8", "landsat7").
            output_path (str): Path to save the resulting index as a GeoTIFF file.
            reference_file (str): Path to a reference raster file for georeferencing and metadata.

        Returns:
            str: Path to the saved GeoTIFF file.
        """
        # Define band mappings for each satellite type
        band_mapping = {
            "landsat7": {"red": 2, "green": 1, "nir": 3, "swir": 4},
            "landsat8": {"red": 3, "green": 2, "nir": 4, "swir": 5},
            "landsat9": {"red": 3, "green": 2, "nir": 4, "swir": 5},
        }

        if satellite_type not in band_mapping:
            raise ValueError(f"Unsupported satellite type: {satellite_type}")

        bands = band_mapping[satellite_type]

        # Convert bands to float for calculations
        if index_type.upper() == "NDVI":
            # NDVI = (NIR - RED) / (NIR + RED)
            nir = matrix[bands["nir"]].astype(np.float32)
            red = matrix[bands["red"]].astype(np.float32)
            index = self._calculate_normalized_difference(nir, red)

        elif index_type.upper() == "NDWI":
            # NDWI = (GREEN - NIR) / (GREEN + NIR)
            green = matrix[bands["green"]].astype(np.float32)
            nir = matrix[bands["nir"]].astype(np.float32)
            index = self._calculate_normalized_difference(green, nir)

        elif index_type.upper() == "SAVI":
            # SAVI = ((NIR - RED) / (NIR + RED + L)) * (1 + L)
            L = 0.5  # Soil adjustment factor
            nir = matrix[bands["nir"]].astype(np.float32)
            red = matrix[bands["red"]].astype(np.float32)
            index = ((nir - red) / (nir + red + L)) * (1 + L)
                
        elif index_type.upper() == "NDBI":
            # NDBI = (SWIR - NIR) / (SWIR + NIR)
            swir = matrix[bands["swir"]].astype(np.float32)
            nir = matrix[bands["nir"]].astype(np.float32)
            index = self._calculate_normalized_difference(swir, nir)
        
        else:
            raise ValueError(f"Unsupported index type: {index_type}")

        # Save the index as a GeoTIFF in the scene folder
        self._save_index_as_geotiff(index, output_path, reference_file)
        
        return output_path

    def _calculate_normalized_difference(self, band1, band2):
        """
        Helper function to calculate a normalized difference index.
        """
        denominator = (band1 + band2)
        return np.divide(
            (band1 - band2), denominator, out=np.zeros_like(denominator), where=denominator != 0
        )

    def _save_index_as_geotiff(self, index, output_path, reference_file):
        """
        Saves the calculated index as a GeoTIFF file.

        Args:
            index (np.ndarray): 2D array of the calculated index.
            output_path (str): Path to save the GeoTIFF file.
            reference_file (str): Path to a reference raster file for metadata.
        """
        with rasterio.open(reference_file) as src:
            meta = src.meta.copy()
            meta.update({
                "dtype": "float32",
                "count": 1,  # Single band for the index
            })

            with rasterio.open(output_path, "w", **meta) as dst:
                dst.write(index, 1)  # Write the index to the first band