# AUTOGENERATED! DO NOT EDIT! File to edit: 02_MLPipeline.ipynb (unless otherwise specified).

__all__ = ['MLPipeline', 'DIRECTORY_PATH', 'TRAIN_FILE', 'TEST_FILE', 'SAMPLE_SUB_FILE', 'scikit_model', 'sci_ml_pl']

# Cell
from .DataFrameLoader import *
from .PreProcessor import *

# Cell
# hide
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, roc_auc_score,accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold


# for displaying diagram of pipelines
from sklearn import set_config
set_config(display="diagram")

# Cell

class MLPipeline:
    """
    Represent MLPipeline class

    Attributes:\n
    pipeline: An MLPipeline instance \n
    dfl: A DataFrameLoader instance \n
    pp: A PreProcessor Instance \n
    model: The given Model
    """

    def __init__(self):
        self.dfl = None
        self.pp = None
        self.model = None
        self.spl = None
        self.transformer_type = None

    def __str__(self):
        """Returns human readable string reprsentation"""
        attr_str = ("spl, dfl, pp, model")
        return ("Training Pipeline object with attributes:"+attr_str)

    def __repr__(self):
        return self.__str__()


    # core methods

    # Bundle preprocessing and modeling code in a training pipeline
    def bundle_preproessor_model(self, transformer_type, model):
        self.spl = Pipeline(
            steps=[('preprocessor', transformer_type),
                   ('model', model)])

    # Core methods for Simple Training
    def prepare_data_for_training(self, train_file_path:str,
                                  test_file_path:str,
                                  idx_col:str, target:str,
                                  random_state:int,
                                  model:object):
        self.model = model

        # call DataFrameLoader module
        self.dfl = DataFrameLoader().from_csv(
            train_file_path=train_file_path,
            test_file_path=test_file_path,
            idx_col=idx_col,
            target=target,
            random_state=random_state)

        # call PreProcessor module
        self.pp = PreProcessor().preprocess_all_cols(
            dataframeloader=self.dfl)

        # call bundle method
        self.bundle_preproessor_model(transformer_type=self.pp.transformer_type,
                                     model = model)
        return self



    def do_cross_validation(self, cv:int, scoring:str):
        scores = cross_val_score(
            estimator=self.spl,
            X=self.dfl.X,
            y=self.dfl.y,
            scoring=scoring,
            cv=cv)
        # Multiply by -1 since sklearn calculates *negative* scoring for some of the metrics
        if "neg_" in scoring:
            scores = -1 * scores
        return scores

    # Core methods for GridSearch
    def do_grid_search(self, param_grid:object, cv:int, scoring:str):

        # create GridSeachCV instance
        grid_search = GridSearchCV(estimator=self.spl,
                                   param_grid=param_grid,
                                   cv=cv,
                                   scoring=scoring)
        # now call fit
        grid_search.fit(self.dfl.X, self.dfl.y)
        return grid_search


    # do k-fold training
    def do_k_fold_training(self, n_splits:int, metrics:object):

        #create stratified K Folds instance
        k_fold = StratifiedKFold(n_splits=n_splits,
                             random_state=48,
                             shuffle=True)

        # list contains metrics score for each fold
        metrics_score = []
        n=0
        for train_idx, valid_idx in k_fold.split(self.dfl.X, self.dfl.y):
            # create X_train
            self.dfl.X_train = self.dfl.X.iloc[train_idx]
            # create X_valid
            self.dfl.X_valid = self.dfl.X.iloc[valid_idx]
            # create y_train
            self.dfl.y_train = self.dfl.y.iloc[train_idx]
            # create y_valid
            self.dfl.y_valid = self.dfl.y.iloc[valid_idx]

            # fit
            self.spl.fit(self.dfl.X_train, self.dfl.y_train)

            #evaluate metrics based upon input
            if "proba" in metrics.__globals__:
                metrics_score.append(metrics(self.dfl.y_valid,
                                               self.spl.predict_proba(self.dfl.X_valid)[:,1]))
            else:
                metrics_score.append(metrics(self.dfl.y_valid,
                                               self.spl.predict(self.dfl.X_valid)))

            print(f"fold: {n+1} , {str(metrics.__name__)}: {metrics_score[n]}")
            # increment fold counter label
            n += 1
        return k_fold, metrics_score

    def do_k_fold_prediction(self, k_fold:object):
        # create preds dataframe
        preds = np.zeros(self.dfl.X_test.shape[0])
        for _ in range(k_fold.n_splits):
            # predict
            preds += self.spl.predict(self.dfl.X_test) / k_fold.n_splits
        return preds

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
    random_state=42)