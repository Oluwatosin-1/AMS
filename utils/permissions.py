from functools import wraps
from django.http import HttpResponseForbidden

def user_type_required(user_type):
    """Decorator for enforcing user type restrictions."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type != user_type:
                return HttpResponseForbidden("Access Denied.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
