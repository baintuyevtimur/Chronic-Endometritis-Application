from django.urls import path
from . import views

app_name = 'chronic_endometritis_app'

urlpatterns = [
    path('chronic_endometritis_app', views.MainView.as_view(), name='main'),
    path(
        'chronic_endometritis_ml_model/',
        views.ChronicEndometritisPredictionView.as_view(),
        name='chronic_endometritis_ml_model'
        ),
]
