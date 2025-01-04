from setuptools import setup, find_packages

setup(
    name="satellite_library",
    version="1.0.0",
    author="Amirhossein Donyadidegan, Mohammad Kord Gholiabadi",
    author_email="amirhossein.donyadidegan@mail.polimi.it, author2@example.com",
    description="A Python library for processing and analyzing satellite data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/satellite-library",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "rasterio>=1.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "sphinx>=4.0",
            "black>=23.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.6",
    keywords="satellite processing, remote sensing, GIS, raster data",
)