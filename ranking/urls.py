from django.urls import path
from . import views

urlpatterns = [
    path("ranks/", views.rank_list, name="rank_list"),
    path("affiliate-rank/", views.affiliate_rank, name="affiliate_rank"),
    path("rewards/", views.view_rewards, name="view_rewards"),  # Rewards view
]
