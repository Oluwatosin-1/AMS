from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from products.views import store
from referrals.views import my_banner
from training.views import feedback, training_materials
from users.views import home

urlpatterns = [
    path('', home, name='home'),
    path('users/', include('users.urls')),  # Include Users app under /users/
    path('admin/', admin.site.urls),
    path('affiliates/', include('affiliates.urls')),
    path('products/', include('products.urls')),
    path('training/', include('training.urls')),
    path('payments/', include('payments.urls')),
    path('referrals/', include('referrals.urls')),
    path('ranking/', include('ranking.urls')),
    path('store/', store, name='store'),
    path('training-materials/', training_materials, name='training_materials'),
    path('my-banner/', my_banner, name='my_banner'),
    path('feedback/',feedback, name='feedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
