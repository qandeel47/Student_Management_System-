from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import AdminCreateTeacherView, MyTeacherProfileView, TeacherViewSet

router = DefaultRouter()
router.register("", TeacherViewSet, basename="teacher")

urlpatterns = [
    path("create/", AdminCreateTeacherView.as_view(), name="teacher-create"),
    path("me/", MyTeacherProfileView.as_view(), name="teacher-me"),
] + router.urls
