from django.urls import path
from .views import register_user, CustomLoginView, CustomLogoutView, affiliate_dashboard

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', affiliate_dashboard, name='affiliate_dashboard'),
]
