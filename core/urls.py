from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', RedirectView.as_view(url='/affiliates/login/', permanent=True), name='home'),  # Redirect to login page
    path('affiliates/', include('affiliates.urls')),  # URLs for Affiliates app
    path('products/', include('products.urls')),  # URLs for Products app
    path('training/', include('training.urls')),  # URLs for Training app
    path('payments/', include('payments.urls')),  # URLs for Payments app
    path('referrals/', include('referrals.urls')),  # URLs for Referrals app
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
