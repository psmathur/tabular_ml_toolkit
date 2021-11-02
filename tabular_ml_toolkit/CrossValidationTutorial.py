# AUTOGENERATED! DO NOT EDIT! File to edit: 03_CrossValidation_Tutorial.ipynb (unless otherwise specified).

__all__ = ['scikit_model', 'sci_ml_pl', 'preds', 'sci_ml_pl', 'scores', 'xgb_model', 'xgb_ml_pl', 'preds', 'xgb_ml_pl',
           'scores']

# Cell
from .MLPipeline import *

# Cell
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# create scikit-learn ml model
scikit_model = RandomForestRegressor(n_estimators=200, random_state=42)

# createm ml pipeline for scikit-learn model
sci_ml_pl = MLPipeline().prepare_data_for_training(
    train_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/train.csv",
    test_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/test.csv",
    idx_col="Id", target="SalePrice",
    model=scikit_model,
    random_state=42,
    valid_size=0.2)

# # Now fit and predict
sci_ml_pl.scikit_pipeline.fit(sci_ml_pl.dataframeloader.X_train, sci_ml_pl.dataframeloader.y_train)

preds = sci_ml_pl.scikit_pipeline.predict(sci_ml_pl.dataframeloader.X_valid)
print('X_valid MAE:', mean_absolute_error(sci_ml_pl.dataframeloader.y_valid, preds))

# Cell
# createm ml pipeline for scikit-learn model
sci_ml_pl = MLPipeline().prepare_data_for_cv(train_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/train.csv",
                                             test_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/test.csv",
                                             idx_col="Id", target="SalePrice",
                                             model=scikit_model,random_state=42,
                                             cv_cols_type = "all") #cv_cols_type = all|num|cat
# Now fit and predict
scores = sci_ml_pl.cross_validation(estimator=sci_ml_pl.scikit_pipeline, cv=5,
                                    scoring='neg_mean_absolute_error')
print("scores:", scores)
print("Average MAE score:", scores.mean())


# Cell
from xgboost import XGBRegressor
# create xgb ml model
xgb_model = XGBRegressor(n_estimators=250,learning_rate=0.05, random_state=42)

# createm ml pipeline for xgb model
xgb_ml_pl = MLPipeline().prepare_data_for_training(
    train_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/train.csv",
    test_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/test.csv",
    idx_col="Id",
    target="SalePrice",
    model=xgb_model,
    random_state=42,
    valid_size=0.2)

# Now fit and predict
xgb_ml_pl.scikit_pipeline.fit(xgb_ml_pl.dataframeloader.X_train, xgb_ml_pl.dataframeloader.y_train)
preds = xgb_ml_pl.scikit_pipeline.predict(xgb_ml_pl.dataframeloader.X_valid)
print('X_valid MAE:', mean_absolute_error(xgb_ml_pl.dataframeloader.y_valid, preds))

# Cell
# createm ml pipeline for scikit-learn model
xgb_ml_pl = MLPipeline().prepare_data_for_cv(train_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/train.csv",
                                             test_file_path= "https://raw.githubusercontent.com/psmathur/tabular_ml_toolkit/master/input/home_data/test.csv",
                                             idx_col="Id", target="SalePrice",
                                             model=xgb_model,random_state=42,
                                             cv_cols_type = "all") #cv_cols_type = all|num|cat
# Now fit and predict
scores = xgb_ml_pl.cross_validation(estimator=xgb_ml_pl.scikit_pipeline, cv=5,
                                    scoring='neg_mean_absolute_error')
print("scores:", scores)
print("Average MAE score:", scores.mean())