from django.urls import path

from .views import (
    AffiliateDashboardView,
    RoleBasedDashboardView,
    affiliate_earnings,
    affiliate_training,
    delete_affiliate,
    generate_referral_link,
    list_affiliate_links, 
    update_affiliate_profile,
    view_downline
)

urlpatterns = [ 
    path('admin_dashboard/', RoleBasedDashboardView.as_view(), name='role_based_dashboard'),
    path('dashboard/', AffiliateDashboardView.as_view(), name='affiliate_dashboard'),
    path('update-profile/', update_affiliate_profile, name='update_affiliate_profile'),
    path('affiliate-links/list/', list_affiliate_links, name='affiliate_links'),
    path('downline/', view_downline, name='view_downline'),  # Add this if missing
    path('referral-link/', generate_referral_link, name='generate_referral_link'),
    path('affiliate-delete/<int:pk>/', delete_affiliate, name='affiliates_affiliate_delete'),
    path('affiliate-earnings/', affiliate_earnings, name='affiliate_earnings'),
    path('affiliate-training/', affiliate_training, name='affiliate_training'),
]
