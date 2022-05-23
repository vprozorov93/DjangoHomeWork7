from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'creator'):
            return request.user.is_superuser or request.user == obj.creator
        else:
            return request.user.is_superuser or request.user == obj.like_user


class IsDraft(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == 'DRAFT':
            return request.user.is_superuser or request.user == obj.creator


