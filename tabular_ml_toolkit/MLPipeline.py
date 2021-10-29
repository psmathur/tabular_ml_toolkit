# AUTOGENERATED! DO NOT EDIT! File to edit: 02_MLPipeline.ipynb (unless otherwise specified).

__all__ = ['MLPipeline']

# Cell
from .DataFrameLoader import *
from .PreProcessor import *

# Cell
# hide
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score

# Cell

class MLPipeline:
    """
    Represent MLPipeline class

    Attributes:\n
    pipeline: An MLPipeline instance \n
    dataframeloader: A DataFrameLoader instance \n
    preprocessor: A PreProcessor Instance \n
    model: The given Model
    """

    def __init__(self):
        self.pipeline = None
        self.dataframeloader = None
        self.preprocessor = None
        self.model = None

    def __str__(self):
        """Returns human readable string reprsentation"""
        attr_str = ("pipeline, dataframeloader, preprocessor, model")
        return ("Training Pipeline object with attributes:"+attr_str)

    def __repr__(self):
        return self.__str__()

#     def __lt__(self):
#         """returns: boolean"""
#         return True

    # core methods
    # Bundle preprocessing and modeling code in a training pipeline
    def bundle_preproessor_model(self, preprocessor:object, model:object):
        self.pipeline = Pipeline(
            steps=[('preprocessor', preprocessor.columns_transfomer),
                   ('model', model)])
#     # return pipeline object
#     def create_pipeline(self, preprocessor:object, model:object):
#         self.bundle_preproessor_model(preprocessor, model)

    def prepare_data_for_training(self, train_file_path:str,
                                  test_file_path:str,
                                  idx_col:str, target:str,
                                  random_state:int,
                                  valid_size:float,
                                  model:object):
        self.model = model
        # call DataFrameLoader module
        self.dataframeloader = DataFrameLoader().from_csv(
            train_file_path=train_file_path,
            test_file_path=test_file_path,
            idx_col=idx_col,target=target,
            random_state=random_state,valid_size=valid_size)
        # call PreProcessor module
        self.preprocessor = PreProcessor().preprocess_data_for_training(
            dataframeloader=self.dataframeloader)

        # call bundle method
        self.bundle_preproessor_model(self.preprocessor, model)
        return self


    def prepare_data_for_cv(self, train_file_path:str, test_file_path:str,
                                          idx_col:str, target:str, model:object,
                                          random_state:int, cv_cols_type:str):
        self.model = model

        # call DataFrameLoader module
        self.dataframeloader = DataFrameLoader().from_csv(
            train_file_path=train_file_path,
            test_file_path=test_file_path,
            idx_col=idx_col, target=target,
            random_state=random_state,
            cv_cols_type=cv_cols_type)

        # call PreProcessor module
        self.preprocessor = PreProcessor().preprocess_data_for_cv(
            cv_cols_type = cv_cols_type,
            dataframeloader=self.dataframeloader)

        # call bundle method
        self.bundle_preproessor_model(self.preprocessor, model)
        return self


    def cross_validation(self,X:object, y:object, cv=5,
                         scoring='neg_mean_absolute_error'):
        # Multiply by -1 since sklearn calculates *negative* MAE
        scores = -1 * cross_val_score(
            estimator=self.pipeline,
            X=self.dataframeloader.X_cv,
            y=self.dataframeloader.y,
            scoring=scoring,
            cv=cv)
        return scores
