from django.urls import path
from .views import (
    ProductDetailView,
    ProductPurchaseView,
    PurchaseSuccessView,
    generate_affiliate_link,
    create_product,
)

urlpatterns = [
    path('links/generate/<int:product_id>/', generate_affiliate_link, name='generate_affiliate_link'),
    # Product details
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    # Product purchase
    path('product/<int:product_id>/purchase/', ProductPurchaseView.as_view(), name='product_purchase'),
    # Generate affiliate link
    path('product/<int:product_id>/generate-link/', generate_affiliate_link, name='generate_affiliate_link'),
    # Create new product (Admin Only)
    path('product/create/', create_product, name='create_product'), 
]

