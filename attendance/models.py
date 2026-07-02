from django.db import models

from courses.models import Course
from students.models import Student
from teachers.models import Teacher


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        LEAVE = "leave", "Leave"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendance_records")
    marked_by = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name="attendance_marked"
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        # A student can only have ONE attendance entry per course per day
        unique_together = ("student", "course", "date")

    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code} - {self.date} - {self.status}"
