from django.urls import path
from .views import payment_history, process_payment, wallet_details, withdraw_request

urlpatterns = [
    path('history/', payment_history, name='payment_history'),
    path('process/<int:payment_id>/', process_payment, name='process_payment'),
    path('wallet-details/', wallet_details, name='wallet_details'),    
    path('withdraw-request/', withdraw_request, name='withdraw_request'),
]
