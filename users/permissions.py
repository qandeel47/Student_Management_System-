from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Allows access only to admin users."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsTeacher(BasePermission):
    """Allows access only to teacher users."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "teacher"
        )


class IsStudent(BasePermission):
    """Allows access only to student users."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "student"
        )


class IsAdminOrReadOnlyForOwner(BasePermission):
    """
    Admin has full access.
    Any other authenticated user can only read (GET/HEAD/OPTIONS).
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role == "admin":
            return True
        return request.method in SAFE_METHODS


class IsAdminOrTeacher(BasePermission):
    """Allows access to admin or teacher users."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("admin", "teacher")
        )


class IsAdminFullOrTeacherReadOnly(BasePermission):
    """
    Admin: full access.
    Teacher: read-only (GET/HEAD/OPTIONS).
    Student: no access at all (students use their own dedicated '/me/' endpoints).
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role == "admin":
            return True
        if request.user.role == "teacher":
            return request.method in SAFE_METHODS
        return False
