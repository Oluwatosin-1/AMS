from django.urls import path

from .views import (
    AffiliateDashboardView,
    RoleBasedDashboardView,
    affiliate_earnings,
    affiliate_training,
    delete_affiliate,
    filter_genealogy_by_rank,
    genealogy_tree_data,
    generate_referral_link,
    list_affiliate_links,
    reset_genealogy,
    update_affiliate_profile,
    view_genealogy,
)

urlpatterns = [
    path(
        "admin_dashboard/",
        RoleBasedDashboardView.as_view(),
        name="role_based_dashboard",
    ),
    path("dashboard/", AffiliateDashboardView.as_view(), name="affiliate_dashboard"),
    path("update-profile/", update_affiliate_profile, name="update_affiliate_profile"),
    path("affiliate-links/list/", list_affiliate_links, name="affiliate_links"),
    path("genealogy/", view_genealogy, name="view_genealogy"),  # Add this if missing
    path("genealogy/reset/", reset_genealogy, name="genealogy_reset"),
    path("genealogy/tree-data/", genealogy_tree_data, name="genealogy_tree_data"),
    path(
        "genealogy/filter/<int:rank_id>/",
        filter_genealogy_by_rank,
        name="genealogy_filter",
    ),
    path("referral-link/", generate_referral_link, name="generate_referral_link"),
    path(
        "affiliate-delete/<int:pk>/",
        delete_affiliate,
        name="affiliates_affiliate_delete",
    ),
    path("affiliate-earnings/", affiliate_earnings, name="affiliate_earnings"),
    path("affiliate-training/", affiliate_training, name="affiliate_training"),
]
