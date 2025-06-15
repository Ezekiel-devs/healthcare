#gérer les permissions d'accès.

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # La redirection vers la page de connexion est gérée par login_required
                return user_passes_test(lambda u: u.is_authenticated)(view_func)(request, *args, **kwargs)

            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Rediriger vers une page "accès refusé" ou le tableau de bord par défaut
                raise PermissionDenied
        return _wrapped_view
    return decorator

patient_required = role_required(allowed_roles=['PATIENT'])
doctor_required = role_required(allowed_roles=['DOCTOR'])