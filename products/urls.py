from django.urls import path
from .views import create_product, generate_affiliate_links, purchase_product

urlpatterns = [
    path('create/', create_product, name='create_product'),
    path('affiliate-links/', generate_affiliate_links, name='affiliate_links'),
    path('purchase/<int:product_id>/', purchase_product, name='purchase_product'),
]
