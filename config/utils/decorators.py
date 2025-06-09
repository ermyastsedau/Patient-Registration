from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.conf import settings

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            print(f"User role: {request.user.role}, Allowed roles: {allowed_roles}")
            if not request.user.is_authenticated:
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
            if request.user.role.upper() not in [r.upper() for r in allowed_roles]:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
