from django.db import models

from courses.models import Course
from departments.models import Department
from users.models import User


class Student(models.Model):
    """
    Extra profile info for a user with role='student'.
    The login account itself lives in the User model; Admin creates both together.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="students"
    )
    courses = models.ManyToManyField(Course, blank=True, related_name="students")
    semester = models.PositiveSmallIntegerField(default=1)
    date_of_birth = models.DateField(blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    guardian_name = models.CharField(max_length=150, blank=True, null=True)
    guardian_phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ["roll_number"]

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name() or self.user.username}"
