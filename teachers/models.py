from django.db import models

from departments.models import Department
from users.models import User


class Teacher(models.Model):
    """
    Extra profile info for a user with role='teacher'.
    The login account itself lives in the User model; Admin creates both together.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="teachers"
    )
    designation = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=150, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["employee_id"]

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"
