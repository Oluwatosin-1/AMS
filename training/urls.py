from django.urls import path
from .views import training_modules, complete_training_module

urlpatterns = [
    path('', training_modules, name='training_modules'),
    path('complete/<int:module_id>/', complete_training_module, name='complete_training_module'),
]