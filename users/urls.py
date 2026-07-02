from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AdminUserCreateView,
    AdminUserDetailView,
    AdminUserListView,
    ChangePasswordView,
    MyProfileView,
)

urlpatterns = [
    # Auth
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login-refresh"),

    # Admin manages accounts
    path("admin/create/", AdminUserCreateView.as_view(), name="admin-user-create"),
    path("admin/list/", AdminUserListView.as_view(), name="admin-user-list"),
    path("admin/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),

    # Self-service
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("me/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
