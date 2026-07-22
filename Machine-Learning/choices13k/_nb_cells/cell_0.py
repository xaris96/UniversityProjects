import json, warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.inspection import permutation_importance
from sklearn.neural_network import MLPRegressor

try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    from catboost import CatBoostRegressor, Pool
except ImportError:
    CatBoostRegressor = None
    Pool = None

SEED = 42
np.random.seed(SEED)

EPS = 1e-9

FAST_MODE = True   # target <10 min while keeping 3+1 models
QUICK_MODE = False  # set True only for very fast iteration
COMPETITION_MODE = True  # slightly stronger search without large time increase
USE_GPU = False    # CPU by default; avoids repeated GPU fallback overhead
EARLY_STOPPING_ROUNDS = 30 if FAST_MODE else 50
WEIGHT_MODE = "sqrt"  # "sqrt" usually gives better MAE than raw uncertainty weights

