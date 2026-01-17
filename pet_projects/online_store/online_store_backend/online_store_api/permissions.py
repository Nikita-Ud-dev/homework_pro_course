from rest_framework.permissions import BasePermission


class IsProductSellerOrAdminOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.seller == user:
            return True
        if user.roles.filter(name_role='admin').exists():
            return True

        return False


class IsCartOrAdminOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.cart.user == user:
            return True
        if user.roles.filter(name_role='admin').exists():
            return True

        return False

class IsOrderOrAdminOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.user == user:
            return True
        if user.roles.filter(name_role='admin').exists():
            return True

        return False


class IsReviewAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.user == user:
            return True
        if user.roles.filter(name_role='admin').exists():
            return True

        return False


class IsSellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name_role__in=['seller', 'admin']).exists()

class IsBuyerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name_role__in=['buyer', 'admin']).exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name_role='admin').exists()