from django.urls import path

 
from .views import referral_list, referral_tree, view_referrals

urlpatterns = [
    path('', referral_list, name='referral_list'),
    path('tree/', referral_tree, name='referral_tree'),
    path('view-referrals/', view_referrals, name='view_referrals'),
]
