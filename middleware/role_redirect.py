from django.shortcuts import redirect
from django.urls import reverse


class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude Django admin URLs
        if request.path.startswith(reverse('admin:index')):
            return self.get_response(request)

        if request.user.is_authenticated:
            current_path = request.path

            # Avoid redirection loops
            if current_path in [
                reverse('admin_dashboard'),
                reverse('affiliate_dashboard'),
            ]:
                return self.get_response(request)

            # Redirect based on user roles
            if request.user.is_superuser:
                return redirect(reverse('admin:index'))  # Django admin
            elif request.user.user_type == 'admin':
                return redirect('admin_dashboard')
            elif request.user.user_type == 'affiliate':
                return redirect('affiliate_dashboard')

        return self.get_response(request)
