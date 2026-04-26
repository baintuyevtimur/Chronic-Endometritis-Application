from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import numpy as np
import pandas as pd
from typing import Dict, Any

from .forms import MLModelForm
from .services.ml_service import MLModelService

# Constants for model features
FEATURES_ML_MODEL = [
    'FSH',
    'SHBG',
    'endometr_thick',
    'CRP',
    'LEP_ADIPOQ',
]

# Initialize ML service
ml_service = MLModelService()


class MainView(View):
    """View for rendering the main page with prediction forms."""

    template_name = 'chronic_endometritis_app/main.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request and render main page with forms.

        Args:
            request: HTTP request object

        Returns:
            Rendered main page with prediction forms
        """
        context = {
            'ml_model_form': MLModelForm(),
        }
        return render(request, self.template_name, context)


class ChronicEndometritisPredictionView(View):
    """View for handling predictions."""

    @method_decorator(require_http_methods(["GET"]))
    def get(self, request: HttpRequest) -> JsonResponse:
        """Handle GET request for prediction.

        Args:
            request: HTTP request object containing prediction parameters

        Returns:
            JsonResponse with prediction results or error message
        """
        try:
            form = MLModelForm(request.GET)

            if not form.is_valid():
                return JsonResponse({'error': form.errors}, status=400)

            input_data = self._prepare_input_data(form.cleaned_data)
            print('input_data', input_data)
            prediction_result = ml_service.make_predict(input_data)

            print(f"Successfully made prediction: {input_data}")
            return JsonResponse(prediction_result)

        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    def _prepare_input_data(self, form_data: Dict[str, Any]) -> np.ndarray:
        """Prepare input data for model prediction.

        Args:
            form_data: Cleaned form data

        Returns:
            Numpy array with prepared input data
        """
        input_values = [
            float(form_data[feature]) for feature in FEATURES_ML_MODEL
            ]
        input_values = np.array(input_values, dtype=float).reshape(1, -1)

        # Проверка соответствия количества значений и названий признаков
        if len(input_values[0]) != len(FEATURES_ML_MODEL):
            raise ValueError(
                f"Количество значений ({len(input_values[0])}) не совпадает"
                "с количеством признаков ({len(FEATURES_ML_MODEL)})"
                )

        # Создаем словарь {название_признака: значение}
        data_dict = {name: [value] for name, value in zip(
            FEATURES_ML_MODEL, input_values[0]
            )}

        # Создаем DataFrame из словаря
        return pd.DataFrame(data_dict)
