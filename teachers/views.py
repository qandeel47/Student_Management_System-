from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.permissions import IsAdmin, IsAdminOrReadOnlyForOwner, IsTeacher
from .models import Teacher
from .serializers import AdminCreateTeacherSerializer, MyTeacherProfileSerializer, TeacherSerializer


@extend_schema_view(
    list=extend_schema(tags=["Teachers"]),
    retrieve=extend_schema(tags=["Teachers"]),
    create=extend_schema(tags=["Teachers"]),
    update=extend_schema(tags=["Teachers"]),
    partial_update=extend_schema(tags=["Teachers"]),
    destroy=extend_schema(tags=["Teachers"]),
)
class TeacherViewSet(viewsets.ModelViewSet):
    """
    Admin: full CRUD on teacher records (list/retrieve/update/delete).
    Use the separate 'create/' endpoint below to add a new teacher (creates login + profile together).
    Teacher/Student: read-only.
    """

    queryset = Teacher.objects.select_related("user", "department").all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForOwner]

    def get_serializer_class(self):
        return TeacherSerializer


@extend_schema(tags=["Teachers"])
class AdminCreateTeacherView(generics.CreateAPIView):
    """Admin creates a new teacher (user account + teacher profile in a single request)."""

    queryset = Teacher.objects.all()
    serializer_class = AdminCreateTeacherSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


@extend_schema(tags=["Teachers"])
class MyTeacherProfileView(generics.RetrieveAPIView):
    """Logged-in teacher views their own profile."""

    serializer_class = MyTeacherProfileSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_object(self):
        if getattr(self, "swagger_fake_view", False):
            return Teacher.objects.none().first()
        return Teacher.objects.select_related("user", "department").get(user=self.request.user)
