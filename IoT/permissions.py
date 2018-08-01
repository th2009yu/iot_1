from rest_framework import permissions


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         # Write permissions are only allowed to the owner of the snippet.
#         return obj.owner == request.user


class IsOwnerOrIsAdminUser(permissions.BasePermission):
    """
    Custom permission only for Owner or AdminUser
    """
    # def has_permission(self, request, view):
    #     if request.user and request.user.is_staff:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        elif request.user and request.user.is_staff:
            return True
        return False


# class IsOwnerOrIsAdminUser1(permissions.BasePermission):
#     """
#     Custom permission only for Owner or AdminUser
#     """
#     # def has_permission(self, request, view):
#     #     if request.user and request.user.is_staff:
#     #         return True
#     #     return False
#
#     def has_object_permission(self, request, view, obj):
#         if obj.Area_number.owner == request.user:
#             return True
#         elif request.user and request.user.is_staff:
#             return True
#         return False




