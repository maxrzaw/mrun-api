from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of objects to edit them.
    """

    def has_object_permission(self, request, view, obj):
        # Read permission allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner.
        return obj.owner == request.user


class CustomCommentPermission(permissions.BasePermission):
    """
    Custom permission to only allow owner or admin to delete a comment.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.auth != None
        
        return obj.user == request.user or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins edit access.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.auth != None
        
        return request.user.is_staff

class IsOwnerAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner or admin to modify a workout.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.auth != None
        
        return obj.owner == request.user or request.user.is_staff
