from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminAttendanceViewSet,
    MarkAttendanceView,
    MyAttendanceListView,
    TeacherAttendanceViewSet,
)

admin_router = DefaultRouter()
admin_router.register("admin", AdminAttendanceViewSet, basename="attendance-admin")

teacher_router = DefaultRouter()
teacher_router.register("teacher", TeacherAttendanceViewSet, basename="attendance-teacher")

urlpatterns = [
    path("mark/", MarkAttendanceView.as_view(), name="attendance-mark"),
    path("me/", MyAttendanceListView.as_view(), name="attendance-me"),
] + admin_router.urls + teacher_router.urls
