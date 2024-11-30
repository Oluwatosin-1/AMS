from django.utils.deprecation import MiddlewareMixin
from products.models import AffiliateProductLink

class ReferralTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ref = request.GET.get('ref')
        if ref:
            request.session['ref'] = ref
