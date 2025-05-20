from django.urls import path
from .views import (
    CustomPasswordResetView,
    create_profile,
    register_user,
    register_admin,
    CustomLoginView,
    custom_logout,
    update_profile,
    view_profile,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path(
        "register/<int:ref>/", register_user, name="register_user_with_ref"
    ),  # Registration with referral
    path("register/admin/", register_admin, name="register_admin"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", custom_logout, name="logout"),  # Use the custom logout view
    path("profile/", view_profile, name="view_profile"),
    path("profile/create/", create_profile, name="create_profile"),
    path("profile/update/", update_profile, name="update_profile"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
]
