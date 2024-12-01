from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/', include('users.urls')),  # Include Users app under /users/
    path('admin/', admin.site.urls),
    path('affiliates/', include('affiliates.urls')),
    path('products/', include('products.urls')),
    path('training/', include('training.urls')),
    path('payments/', include('payments.urls')),
    path('referrals/', include('referrals.urls')),
    path('ranking/', include('ranking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
