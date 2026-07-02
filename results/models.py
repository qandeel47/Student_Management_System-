from django.core.validators import MinValueValidator
from django.db import models

from courses.models import Course
from students.models import Student
from teachers.models import Teacher


class Result(models.Model):
    class ExamType(models.TextChoices):
        QUIZ = "quiz", "Quiz"
        ASSIGNMENT = "assignment", "Assignment"
        MIDTERM = "midterm", "Midterm"
        FINAL = "final", "Final"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="results")
    uploaded_by = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name="results_uploaded"
    )
    exam_type = models.CharField(max_length=15, choices=ExamType.choices, default=ExamType.FINAL)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "course", "exam_type")

    @property
    def percentage(self) -> float:
        if self.total_marks:
            return round((float(self.marks_obtained) / float(self.total_marks)) * 100, 2)
        return 0

    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code} - {self.exam_type}"
