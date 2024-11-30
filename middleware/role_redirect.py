# middleware/role_redirect.py

from django.shortcuts import redirect

class RoleRedirectMiddleware:
    """
    Middleware to redirect users based on their role after login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip processing if user is not authenticated
        if request.user.is_authenticated:
            if request.user.user_type == 'admin':
                return redirect('/admin-dashboard/')  # Replace with your admin dashboard URL
            elif request.user.user_type == 'affiliate':
                return redirect('/affiliate-dashboard/')  # Replace with your affiliate dashboard URL
        return self.get_response(request)
