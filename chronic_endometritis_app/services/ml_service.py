import os
import xgboost as xgb
import numpy as np
import pandas as pd
from typing import Dict, Any


class MLModelService:
    """Service for handling machine learning model operations."""

    def __init__(self):
        """Initialize the ML service with pre-trained models."""
        self.ml_model_path = os.path.join('ml_models', 'm5.json')
        self.ml_model = None
        self.ml_model_num_features = None
        self._load_models()

    def _load_models(self) -> None:
        """Load the XGBoost models from files."""
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))

            # Load before delivery model with labs parametres
            ml_model_full_path = os.path.join(base_dir, self.ml_model_path)
            self.ml_model = xgb.XGBClassifier()
            self.ml_model.load_model(ml_model_full_path)

            print("Successfully loaded ML model")
        except Exception as e:
            print(f"Error loading ML model: {str(e)}")
            raise RuntimeError("Failed to load ML model")

    def make_predict(self, input_data: np.ndarray) -> Dict[str, Any]:
        """Make prediction using the model.

        Args:
            input_data: Numpy array of shape (1, n_features) containing the
            input features

        Returns:
            Dictionary containing prediction and probability scores
        """
        input_data = pd.DataFrame(input_data, columns=input_data.columns)

        prediction = self.ml_model.predict(input_data)
        probabilities = self.ml_model.predict_proba(input_data)

        return {
            'prediction': int(prediction[0]),
            'probability': probabilities.tolist()
        }
