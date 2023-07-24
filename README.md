# MLOps Project Car Prices Prediction

![car](https://github.com/benitomartin/templates/assets/116911431/d5d98b26-f096-42bf-b97d-d2fefdebe555)

This project is currently being developed as part [MLOps Zoomcamp] (https://github.com/DataTalksClub/mlops-zoomcamp) course provided by [DataTalks](https://datatalks.club/).Club.

The dataset used has been downloaded from [Kaggle](https://www.kaggle.com/datasets/hellbuoy/car-price-prediction) and a preliminary data analysis was performed (see `notebooks` folder), to get some insights for the further project development.

Feel free to close this repo :wink:

## Project Set Up

1. Clone the repo:

   ```bash
   git clone https://github.com/benitomartin/mlops-car-prices.git

2. Create the virtual environment named `main-env` using Conda with Python version 3.9:

   ```bash
   conda create -n main-env python=3.9
   conda activate main-env

3. Install `setuptools` and `wheel`:

    ```bash
    conda install setuptools wheel

4. Execute the setup.py script and install the project dependencies included in the requirements.txt:

    ```bash
    pip install .

    or
 
    make install