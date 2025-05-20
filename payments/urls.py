from django.urls import path

from products.views import PurchaseSuccessView
from .views import (
    initialize_payment,
    invoice_download,
    payment_callback,
    payment_history,
    process_payment,
    wallet_details,
    withdraw_request,
)

urlpatterns = [
    path("history/", payment_history, name="payment_history"),
    path("process/<int:payment_id>/", process_payment, name="process_payment"),
    path("wallet-details/", wallet_details, name="wallet_details"),
    path("withdraw-request/", withdraw_request, name="withdraw_request"),
    path("initialize/<int:product_id>/", initialize_payment, name="initialize_payment"),
    path("callback/", payment_callback, name="payment_callback"),
    path("invoice/<int:purchase_id>/", invoice_download, name="invoice_download"),
    path("success/", PurchaseSuccessView.as_view(), name="purchase_success"),
]
