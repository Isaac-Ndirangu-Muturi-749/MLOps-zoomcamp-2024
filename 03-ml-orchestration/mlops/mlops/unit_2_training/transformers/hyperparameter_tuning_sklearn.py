
from typing import Callable, Dict, Tuple, Union
from pandas import Series
from scipy.sparse._csr import csr_matrix
from sklearn.base import BaseEstimator
from mlops.utils.models.sklearn import load_class, tune_hyperparameters

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

@transformer
def hyperparameter_tuning(
    model_class_name: str,
    training_set: Dict[str, Union[Series, csr_matrix]],
    *args,
    **kwargs,
) -> Callable[..., BaseEstimator]:
    # Debugging print statements to check the structure of training_set
    print("Training set structure:", training_set)

    # Ensure 'build' is a key in training_set
    if 'build' not in training_set:
        raise ValueError("The key 'build' is missing in the training_set dictionary.")
    
    build_set = training_set['build']

    # Check the type of build_set
    if not isinstance(build_set, (list, tuple)):
        raise TypeError(f"Expected 'build' to be a list or tuple, got {type(build_set)}.")

    # Check the length of build_set
    if len(build_set) != 7:
        raise ValueError(f"Expected 'build' to have 7 elements, got {len(build_set)}.")
    
    X, X_train, X_val, y, y_train, y_val, _ = build_set

    # Additional debugging prints
    print(f"X: {type(X)}, X_train: {type(X_train)}, X_val: {type(X_val)}")
    print(f"y: {type(y)}, y_train: {type(y_train)}, y_val: {type(y_val)}")

    model_class = load_class(model_class_name)

    hyperparameters = tune_hyperparameters(
        model_class,
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        max_evaluations=kwargs.get('max_evaluations'),
        random_state=kwargs.get('random_state'),
    )

    return hyperparameters, X, y, dict(cls=model_class, name=model_class_name)

# Ensure that you are passing the correct 'training_set' to this function
