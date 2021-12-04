# AUTOGENERATED! DO NOT EDIT! File to edit: utility.ipynb (unless otherwise specified).

__all__ = ['find_ideal_cpu_cores', 'check_has_n_jobs', 'fetch_tabnet_params_for_problem_type',
           'fetch_xgb_params_for_problem_type', 'fetch_skl_params_for_problem_type', 'kfold_dict_mean']

# Cell
from .dataframeloader import *
from .preprocessor import *
from .logger import *
from .xgb_optuna_objective import *

# Cell
# hide

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss, f1_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold

# for Optuna
import optuna

#for XGB
import xgboost

#for TabNet
from pytorch_tabnet.tab_model import TabNetClassifier, TabNetRegressor
from pytorch_tabnet.multitask import TabNetMultiTaskClassifier

# for finding n_jobs in all sklearn estimators
from sklearn.utils import all_estimators
import inspect

# Just to compare fit times
import time

# for os specific settings
import os

# Cell

#helper method to find ideal cpu cores
def find_ideal_cpu_cores():
    if os.cpu_count() > 2:
        ideal_cpu_cores = os.cpu_count()-1
        logger.info(f"{os.cpu_count()} cores found, model and data parallel processing should worked!")
    else:
        ideal_cpu_cores = None
        logger.info(f"{os.cpu_count()} cores found, model and data parallel processing may NOT worked!")
    return ideal_cpu_cores

#Helper method to find all sklearn estimators with support for parallelism aka n_jobs
def check_has_n_jobs():
    has_n_jobs = ['XGBRegressor', 'XGBClassifier']
    for est in all_estimators():
        s = inspect.signature(est[1])
        if 'n_jobs' in s.parameters:
            has_n_jobs.append(est[0])
    return has_n_jobs

# Cell

def fetch_tabnet_params_for_problem_type(problem_type):
    if problem_type == "binary_classification":
        tabnet_model = TabNetClassifier
        direction = "maximize"
        eval_metric = "auc"
        val_preds_metrics = [roc_auc_score, log_loss, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "multi_label_classification":
        tabnet_model = TabNetClassifier
        direction = "maximize"
        eval_metric = "auc"
        val_preds_metrics = [roc_auc_score, log_loss, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "multi_class_classification":
        tabnet_model = TabNetMultiTaskClassifier
        direction = "minimize"
        eval_metric = "logloss"
        val_preds_metrics = [log_loss, roc_auc_score, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "regression":
        tabnet_model = TabNetRegression
        direction = "minimize"
        eval_metric = "rmse"
        val_preds_metrics = [mean_absolute_error, mean_squared_error, r2_score]
    else:
        raise NotImplementedError

    return tabnet_model, val_preds_metrics, eval_metric, direction

def fetch_xgb_params_for_problem_type(problem_type):
    if problem_type == "binary_classification":
        xgb_model = xgboost.XGBClassifier
        direction = "maximize"
        eval_metric = "auc"
        val_preds_metrics = [roc_auc_score, log_loss, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "multi_label_classification":
        xgb_model = xgboost.XGBClassifier
        direction = "maximize"
        eval_metric = "auc"
        val_preds_metrics = [roc_auc_score, log_loss, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "multi_class_classification":
        xgb_model = xgboost.XGBClassifier
        direction = "minimize"
        eval_metric = "mlogloss"
        val_preds_metrics = [log_loss, roc_auc_score, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "regression":
        xgb_model = xgboost.XGBRegressor
        direction = "minimize"
        eval_metric = "rmse"
        val_preds_metrics = [mean_absolute_error, mean_squared_error, r2_score]
    else:
        raise NotImplementedError

    return xgb_model, val_preds_metrics, eval_metric, direction

def fetch_skl_params_for_problem_type(problem_type):
    if problem_type == "binary_classification":
        direction = "maximize"
        val_preds_metrics = [roc_auc_score, log_loss, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "multi_label_classification":
        direction = "maximize"
        val_preds_metrics = [roc_auc_score, log_loss, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "multi_class_classification":
        direction = "minimize"
        val_preds_metrics = [log_loss, roc_auc_score, accuracy_score, f1_score, precision_score, recall_score]

    elif problem_type == "regression":
        direction = "minimize"
        val_preds_metrics = [mean_absolute_error, mean_squared_error, r2_score]
    else:
        raise NotImplementedError

    return val_preds_metrics, direction


def kfold_dict_mean(kfold_metrics_results):
    mean_metrics_results = {}
    for single_fold_metrics_results in kfold_metrics_results:
        for key in single_fold_metrics_results.keys():
            if key in mean_metrics_results:
                mean_metrics_results[key] += single_fold_metrics_results[key] / len(kfold_metrics_results)
            else:
                mean_metrics_results[key] = single_fold_metrics_results[key] / len(kfold_metrics_results)

    return mean_metrics_results