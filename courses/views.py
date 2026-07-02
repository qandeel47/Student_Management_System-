from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.permissions import IsAdminOrReadOnlyForOwner
from .models import Course
from .serializers import CourseSerializer


@extend_schema_view(
    list=extend_schema(tags=["Courses"]),
    retrieve=extend_schema(tags=["Courses"]),
    create=extend_schema(tags=["Courses"]),
    update=extend_schema(tags=["Courses"]),
    partial_update=extend_schema(tags=["Courses"]),
    destroy=extend_schema(tags=["Courses"]),
)
class CourseViewSet(viewsets.ModelViewSet):
    """
    Admin: full CRUD.
    Teacher/Student: read-only (list & retrieve).
    """

    queryset = Course.objects.select_related("department", "teacher__user").all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForOwner]
    filterset_fields = ["department", "teacher"]
