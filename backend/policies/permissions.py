from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class PolicyPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
            
        
        return request.user.role in ['admin', 'manager']