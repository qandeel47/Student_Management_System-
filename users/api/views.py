from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from ..models import User
from ..permissions import IsAdmin
from .serializers import (
    AdminCreateUserSerializer,
    ChangePasswordSerializer,
    MyProfileSerializer,
    UserSerializer,
)


@extend_schema(tags=["Users (Admin)"])
class AdminUserCreateView(generics.CreateAPIView):
    """Admin creates a login account for a teacher or student."""

    queryset = User.objects.all()
    serializer_class = AdminCreateUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


@extend_schema(tags=["Users (Admin)"])
class AdminUserListView(generics.ListAPIView):
    """Admin views all user accounts."""

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


@extend_schema(tags=["Users (Admin)"])
class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin retrieves, updates, or deactivates a specific user account."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


@extend_schema(tags=["My Account"])
class MyProfileView(generics.RetrieveUpdateAPIView):
    """Any logged-in user (admin/teacher/student) views or updates their own basic info."""

    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["My Account"])
class ChangePasswordView(APIView):
    """Any logged-in user changes their own password."""

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
