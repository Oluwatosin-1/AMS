from django.urls import path
from .views import delete_training_module, start_training, training_modules, complete_training_module, verify_training_completion

urlpatterns = [ 
    path('training/delete/<int:pk>/', delete_training_module, name='training_trainingmodule_delete'), 
    path('training-modules/', training_modules, name='training_modules'),
    path('start-training/<int:module_id>/', start_training, name='start_training'),
    path('complete-training/<int:module_id>/', complete_training_module, name='complete_training_module'),
    path('verify-training/<int:progress_id>/', verify_training_completion, name='verify_training_completion'),

]
