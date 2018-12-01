from rest_framework.permissions import BasePermission, AllowAny
from .contrib.models import User as UserM


_ = AllowAny



class DenyAny(BasePermission):


    def has_permission(self, request, view):
        return False



class IsSTokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        try:
            return isinstance(request.user, UserM)
        except:
            return False
