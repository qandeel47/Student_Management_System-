from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from students.models import Student
from users.permissions import IsAdmin, IsStudent, IsTeacher
from ..models import Attendance
from .serializers import AttendanceSerializer, MarkAttendanceSerializer, MyAttendanceSerializer


@extend_schema_view(
    list=extend_schema(tags=["Attendance (Admin)"]),
    retrieve=extend_schema(tags=["Attendance (Admin)"]),
    update=extend_schema(tags=["Attendance (Admin)"]),
    partial_update=extend_schema(tags=["Attendance (Admin)"]),
    destroy=extend_schema(tags=["Attendance (Admin)"]),
)
class AdminAttendanceViewSet(viewsets.ModelViewSet):
    """Admin: full visibility and control over all attendance records."""

    queryset = Attendance.objects.select_related("student__user", "course", "marked_by__user").all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filterset_fields = ["student", "course", "date", "status"]
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]


@extend_schema(tags=["Attendance (Teacher)"])
class MarkAttendanceView(generics.CreateAPIView):
    """Teacher marks attendance for a student in one of the courses they teach."""

    queryset = Attendance.objects.all()
    serializer_class = MarkAttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


@extend_schema_view(
    list=extend_schema(tags=["Attendance (Teacher)"]),
    retrieve=extend_schema(tags=["Attendance (Teacher)"]),
    update=extend_schema(tags=["Attendance (Teacher)"]),
    partial_update=extend_schema(tags=["Attendance (Teacher)"]),
)
class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    """Teacher views/updates attendance records they personally marked."""

    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    filterset_fields = ["student", "course", "date", "status"]
    http_method_names = ["get", "put", "patch", "head", "options"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Attendance.objects.none()
        return Attendance.objects.select_related("student__user", "course").filter(
            marked_by__user=self.request.user
        )


@extend_schema(tags=["Attendance (Student)"])
class MyAttendanceListView(generics.ListAPIView):
    """Student views their own attendance history — read-only."""

    serializer_class = MyAttendanceSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    filterset_fields = ["course", "status", "date"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Attendance.objects.none()
        student = Student.objects.get(user=self.request.user)
        return Attendance.objects.filter(student=student).select_related("course")
