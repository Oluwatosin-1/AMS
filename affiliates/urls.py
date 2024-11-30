from django.urls import path
from .views import affiliate_earnings, affiliate_links, affiliate_training, register_admin, register_user, CustomLoginView, CustomLogoutView, affiliate_dashboard, admin_dashboard, update_affiliate_profile

urlpatterns = [
    path('register/', register_user, name='register'),
    path('register-admin/', register_admin, name='register_admin'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', affiliate_dashboard, name='affiliate_dashboard'),
    path('affiliate-dashboard/', affiliate_dashboard, name='affiliate_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'), 
    path('update-profile/', update_affiliate_profile, name='update_affiliate_profile'),  
    path('update-profile/', update_affiliate_profile, name='update_affiliate_profile'),
    path('affiliate-links/', affiliate_links, name='affiliate_links'),
    path('affiliate-earnings/', affiliate_earnings, name='affiliate_earnings'),
    path('affiliate-training/', affiliate_training, name='affiliate_training'),
]
