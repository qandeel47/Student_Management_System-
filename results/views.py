from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from students.models import Student
from users.permissions import IsAdmin, IsStudent, IsTeacher
from .models import Result
from .serializers import MyResultSerializer, ResultSerializer, UploadResultSerializer


@extend_schema_view(
    list=extend_schema(tags=["Results (Admin)"]),
    retrieve=extend_schema(tags=["Results (Admin)"]),
    update=extend_schema(tags=["Results (Admin)"]),
    partial_update=extend_schema(tags=["Results (Admin)"]),
    destroy=extend_schema(tags=["Results (Admin)"]),
)
class AdminResultViewSet(viewsets.ModelViewSet):
    """Admin: full visibility and control over all results."""

    queryset = Result.objects.select_related("student__user", "course", "uploaded_by__user").all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_fields = ["student", "course", "exam_type"]
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]


@extend_schema(tags=["Results (Teacher)"])
class UploadResultView(generics.CreateAPIView):
    """Teacher uploads a result for a student in one of the courses they teach."""

    queryset = Result.objects.all()
    serializer_class = UploadResultSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


@extend_schema_view(
    list=extend_schema(tags=["Results (Teacher)"]),
    retrieve=extend_schema(tags=["Results (Teacher)"]),
    update=extend_schema(tags=["Results (Teacher)"]),
    partial_update=extend_schema(tags=["Results (Teacher)"]),
)
class TeacherResultViewSet(viewsets.ModelViewSet):
    """Teacher views/updates results they personally uploaded."""

    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    filterset_fields = ["student", "course", "exam_type"]
    http_method_names = ["get", "put", "patch", "head", "options"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Result.objects.none()
        return Result.objects.select_related("student__user", "course").filter(
            uploaded_by__user=self.request.user
        )


@extend_schema(tags=["Results (Student)"])
class MyResultListView(generics.ListAPIView):
    """Student views their own results — read-only."""

    serializer_class = MyResultSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    filterset_fields = ["course", "exam_type"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Result.objects.none()
        student = Student.objects.get(user=self.request.user)
        return Result.objects.filter(student=student).select_related("course")
