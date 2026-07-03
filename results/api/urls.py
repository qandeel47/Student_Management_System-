from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminResultViewSet,
    MyResultListView,
    TeacherResultViewSet,
    UploadResultView,
)

admin_router = DefaultRouter()
admin_router.register("admin", AdminResultViewSet, basename="result-admin")

teacher_router = DefaultRouter()
teacher_router.register("teacher", TeacherResultViewSet, basename="result-teacher")

urlpatterns = [
    path("upload/", UploadResultView.as_view(), name="result-upload"),
    path("me/", MyResultListView.as_view(), name="result-me"),
] + admin_router.urls + teacher_router.urls
