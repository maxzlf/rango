from rest_framework.permissions import BasePermission

from .models import User



class IsSTokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User)
