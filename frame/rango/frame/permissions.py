from rest_framework.permissions import BasePermission, AllowAny

from .consts import BaseConst
from .contrib.models import User as UserM
from .contrib.models import SToken


_ = AllowAny



class DenyAny(BasePermission):


    def has_permission(self, request, view):
        return False



class IsSTokenAuthenticated(BasePermission):


    def has_permission(self, request, view):
        try:
            return isinstance(request.user, UserM) and \
                   isinstance(request.stoken, SToken)
        except:
            return False



class IsDebugMode(BasePermission):


    def has_permission(self, request, view):
        base_const = BaseConst(view.const_accessor)
        return base_const.debug_mode



class IsActivated(BasePermission):


    def has_permission(self, request, view):
        base_const = BaseConst(view.const_accessor)
        return base_const.activated
