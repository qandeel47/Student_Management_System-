from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

from users.permissions import IsAdminOrReadOnlyForOwner
from ..models import Department
from .serializers import DepartmentSerializer


@extend_schema_view(
    list=extend_schema(tags=["Departments"]),
    retrieve=extend_schema(tags=["Departments"]),
    create=extend_schema(tags=["Departments"]),
    update=extend_schema(tags=["Departments"]),
    partial_update=extend_schema(tags=["Departments"]),
    destroy=extend_schema(tags=["Departments"]),
)
class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Admin: full CRUD.
    Teacher/Student: read-only (list & retrieve).
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForOwner]
