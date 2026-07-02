from django.db import models

from departments.models import Department
from teachers.models import Teacher


class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses"
    )
    credit_hours = models.PositiveSmallIntegerField(default=3)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"
