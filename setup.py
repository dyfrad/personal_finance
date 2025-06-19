from setuptools import setup, find_packages
import sys
from pathlib import Path

# Add project root to Python path to import version
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.version import (
    __version__, __app_name__, __author__, __author_email__, 
    __github_url__, __package_name__, __entry_point__, __description__
)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__github_url__,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            f"{__entry_point__}=main:main",
        ],
    },
) 