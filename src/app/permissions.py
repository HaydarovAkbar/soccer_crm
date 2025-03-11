from rest_framework.permissions import BasePermission


class FieldOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_groups = request.user.groups.all()
        if user_groups.filter(name='owner_field').exists():
            return obj.user == request.user
        return False


class CustomUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_groups = request.user.groups.all()
        if user_groups.filter(name='custom_user').exists():
            return obj == request.user
        return False
