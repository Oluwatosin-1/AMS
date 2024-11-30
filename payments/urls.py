from django.urls import path
from .views import payment_history, process_payment

urlpatterns = [
    path('history/', payment_history, name='payment_history'),
    path('process/<int:payment_id>/', process_payment, name='process_payment'),
]
