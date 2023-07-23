# MLOps Project Cars Price Prediction

## Project Set Up

1. Clone the repo:

   ```bash
   git clone https://github.com/benitomartin/mlops-car-prices.git

2. Create the virtual environment named `main-env` using Conda with Python version 3.9:

   ```bash
   conda create -n main-env python=3.9
   conda activate main-env

3. If `python-dotenv` is not workinng, you need to install it in the project:

    ```bash
    conda install -c conda-forge python-dotenv
    conda install -n myenv setuptools wheel

4. Execute the setup.py script and install the project dependencies incl. requirements.txt (if you face an error with `python-dotenv`, use `BASE_DIR` in the `setup.py` as a string).

    ```bash
    pip install .

    or
 
    make install