from rest_framework import permissions


class ReservationPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
