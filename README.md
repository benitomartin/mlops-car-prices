# MLOps Project Cars Price Prediction

## Project Set Up

1. Clone the repo:

   ```bash
   git clone https://github.com/benitomartin/mlops-car-prices.git

2. Create the virtual environment named `main-env` using Conda with Python version 3.9:

   ```bash
   conda create -n main-env python=3.9
   conda activate main-env

3. If `setuptools` and `wheel` is not workinng, you need to install it in the project:

    ```bash
    conda install setuptools wheel

4. Execute the setup.py script and install the project dependencies included in lsrequirements.txt:

    ```bash
    pip install .

    or
 
    make install