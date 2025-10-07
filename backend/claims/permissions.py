from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class ClaimCreationPermission(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated 
            and request.user.role in ['call_center', 'manager', 'admin']
        )


class ClaimPermissions(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
            
        if obj.status == 'reported':
            return request.user.role in ['call_center', 'admin', 'manager']
        else:
            return request.user.role in ['admin', 'manager', 'senior_adjuster', 'adjuster']


class AssignClaimPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return (
            request.user.is_authenticated 
            and request.user.role in ['admin', 'manager', 'call_center']
        )


class CreateClaimNotePermission(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated 
            and request.user.role in ['admin', 'manager', 'senior_adjuster', 'adjuster']
        )


class CreateClaimDocumentPermission(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated 
            and request.user.role in ['admin', 'manager', 'senior_adjuster', 'adjuster']
        )


class ClaimNotePermissions(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
            
        # Admins and managers can edit any note
        if request.user.role in ['admin', 'manager']:
            return True
        
        # Adjusters can only edit their own notes
        return (
            obj.author == request.user 
            and request.user.role in ['adjuster', 'senior_adjuster']
        )


class ClaimDocumentPermissions(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
            
        # Admins and managers can edit any document
        if request.user.role in ['admin', 'manager']:
            return True
        
        # Adjusters can only edit their own documents
        return (
            obj.uploaded_by == request.user 
            and request.user.role in ['adjuster', 'senior_adjuster']
        )


class UpdateClaimStatusPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return (
            request.user.is_authenticated 
            and request.user.role in ['admin', 'manager', 'senior_adjuster', 'adjuster']
        )