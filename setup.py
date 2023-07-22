## setup.py file

# Importing necessary functions from setuptools
import os
from pathlib import Path
from setuptools import find_packages, find_namespace_packages, setup
from dotenv import load_dotenv


# Load environmental variables
load_dotenv()

# Get the current directory path as BASE_DIR
BASE_DIR = Path(os.getenv('BASE_DIR'))

# Reading the requirements from the "requirements.txt" file
with open(BASE_DIR / "requirements.txt", "r", encoding="Windows-1252") as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

# Setting up the package metadata and dependencies
setup(
    name='mlops-project-cars-prices',
    description="Car Prices MLOps Project",
    version='1.0',
    author="Benito Martin",
    install_requires=requirements,
    packages=find_packages() + find_namespace_packages(),
)

