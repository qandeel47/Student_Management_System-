from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import AdminCreateStudentView, MyStudentProfileView, StudentViewSet

router = DefaultRouter()
router.register("", StudentViewSet, basename="student")

urlpatterns = [
    path("create/", AdminCreateStudentView.as_view(), name="student-create"),
    path("me/", MyStudentProfileView.as_view(), name="student-me"),
] + router.urls
