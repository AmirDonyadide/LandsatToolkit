"""
Helper Functions

This module provides common utility functions used across the library.
"""

import os
import numpy as np


def calculate_normalized_difference(band1, band2):
    """
    Calculates a normalized difference index between two bands.

    Args:
        band1 (np.ndarray): First band as a 2D NumPy array.
        band2 (np.ndarray): Second band as a 2D NumPy array.

    Returns:
        np.ndarray: Normalized difference index as a 2D NumPy array.
    """
    denominator = band1 + band2
    return np.divide(
        band1 - band2, denominator, out=np.zeros_like(denominator), where=denominator != 0
    )


def ensure_directory_exists(directory_path):
    """
    Ensures that the specified directory exists. Creates it if it doesn't.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def log_message(message, level="INFO"):
    """
    Logs a message with a specified log level.

    Args:
        message (str): The message to log.
        level (str): The log level (e.g., "INFO", "WARNING", "ERROR"). Default is "INFO".

    Returns:
        None
    """
    print(f"[{level}] {message}")


def clip_values_to_range(array, min_value, max_value):
    """
    Clips the values in a NumPy array to a specified range.

    Args:
        array (np.ndarray): The input array.
        min_value (float): The minimum allowable value.
        max_value (float): The maximum allowable value.

    Returns:
        np.ndarray: Array with values clipped to the specified range.
    """
    return np.clip(array, min_value, max_value)