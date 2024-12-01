from django.urls import path
from .views import create_profile, register_user, register_admin, CustomLoginView, custom_logout, update_profile, view_profile

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('register/<int:ref>/', register_user, name='register_user_with_ref'),  # Registration with referral
    path('register/admin/', register_admin, name='register_admin'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),  # Use the custom logout view
    path('profile/', view_profile, name='view_profile'),
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/update/', update_profile, name='update_profile'),
]
