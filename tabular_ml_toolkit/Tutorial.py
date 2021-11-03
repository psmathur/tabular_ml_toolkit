# AUTOGENERATED! DO NOT EDIT! File to edit: 03_Tutorial.ipynb (unless otherwise specified).

__all__ = ['DIRECTORY_PATH', 'TRAIN_FILE', 'TEST_FILE', 'SAMPLE_SUB_FILE', 'scikit_model', 'sci_ml_pl', 'sci_ml_pl',
           'xgb_model', 'xgb_ml_pl']

# Cell
from .MLPipeline import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np
from sklearn import set_config
set_config(display="diagram")

# Cell
# Dataset file names and Paths
DIRECTORY_PATH = "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/"
TRAIN_FILE = "train.csv"
TEST_FILE = "test.csv"
SAMPLE_SUB_FILE = "sample_submission.csv"

# Cell

# create scikit-learn ml model
scikit_model = RandomForestRegressor(n_estimators=200, random_state=42)

# createm ml pipeline for scikit-learn model
sci_ml_pl = MLPipeline().prepare_data_for_training(
    train_file_path= DIRECTORY_PATH+TRAIN_FILE,
    test_file_path= DIRECTORY_PATH+TEST_FILE,
    idx_col="Id", target="SalePrice",
    model=scikit_model,
    random_state=42,
    valid_size=0.2)

# Cell
# createm ml pipeline for scikit-learn model without valid_size i.e. no split, so X,y remain original size
sci_ml_pl = MLPipeline().prepare_data_for_training(
    train_file_path= DIRECTORY_PATH+TRAIN_FILE,
    test_file_path= DIRECTORY_PATH+TEST_FILE,
    idx_col="Id",
    target="SalePrice",
    model=scikit_model,
    random_state=42)

# Cell
from xgboost import XGBRegressor
# create xgb ml model
xgb_model = XGBRegressor(n_estimators=250,learning_rate=0.05, random_state=42)

# createm ml pipeline for xgb model
xgb_ml_pl = MLPipeline().prepare_data_for_training(
    train_file_path= DIRECTORY_PATH+TRAIN_FILE,
    test_file_path= DIRECTORY_PATH+TEST_FILE,
    idx_col="Id",
    target="SalePrice",
    model=xgb_model,
    random_state=42,
    valid_size=0.2)