from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.permissions import IsAdmin, IsAdminFullOrTeacherReadOnly, IsStudent
from ..models import Student
from .serializers import AdminCreateStudentSerializer, MyStudentProfileSerializer, StudentSerializer


@extend_schema_view(
    list=extend_schema(tags=["Students"]),
    retrieve=extend_schema(tags=["Students"]),
    create=extend_schema(tags=["Students"]),
    update=extend_schema(tags=["Students"]),
    partial_update=extend_schema(tags=["Students"]),
    destroy=extend_schema(tags=["Students"]),
)
class StudentViewSet(viewsets.ModelViewSet):
    """
    Admin: full CRUD on student records (list/retrieve/update/delete).
    Use the separate 'create/' endpoint below to add a new student (creates login + profile together).
    Teacher: read-only (e.g. to see who's enrolled).
    Student: no access here — students use their own '/me/' endpoint instead.
    """

    queryset = Student.objects.select_related("user", "department").prefetch_related("courses").all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminFullOrTeacherReadOnly]
    filterset_fields = ["department", "semester"]


@extend_schema(tags=["Students"])
class AdminCreateStudentView(generics.CreateAPIView):
    """Admin creates a new student (user account + student profile in a single request)."""

    queryset = Student.objects.all()
    serializer_class = AdminCreateStudentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


@extend_schema(tags=["Students"])
class MyStudentProfileView(generics.RetrieveAPIView):
    """Logged-in student views their own profile — read-only, cannot edit their own record."""

    serializer_class = MyStudentProfileSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_object(self):
        if getattr(self, "swagger_fake_view", False):
            return Student.objects.none().first()
        return Student.objects.select_related("user", "department").prefetch_related("courses").get(
            user=self.request.user
        )
