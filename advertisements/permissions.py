from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj.creator


class IsDraft(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == 'DRAFT':
            return request.user.is_superuser or request.user == obj.creator


