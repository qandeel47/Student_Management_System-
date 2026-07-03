from django.db import IntegrityError
from rest_framework import serializers

from ..models import Result


class ResultSerializer(serializers.ModelSerializer):
    """Full representation used for listing/retrieving (admin & teacher)."""

    student_roll_number = serializers.CharField(source="student.roll_number", read_only=True)
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)
    uploaded_by_name = serializers.CharField(source="uploaded_by.user.get_full_name", read_only=True)
    percentage = serializers.ReadOnlyField()

    class Meta:
        model = Result
        fields = [
            "id", "student", "student_roll_number", "student_name",
            "course", "course_code", "uploaded_by", "uploaded_by_name",
            "exam_type", "marks_obtained", "total_marks", "percentage",
            "remarks", "created_at",
        ]
        read_only_fields = ["uploaded_by", "created_at"]


class UploadResultSerializer(serializers.ModelSerializer):
    """
    Used by a Teacher to upload/record a result for a student in one of their own courses.
    'uploaded_by' is set automatically from the logged-in teacher.
    """

    class Meta:
        model = Result
        fields = ["id", "student", "course", "exam_type", "marks_obtained", "total_marks", "remarks"]

    def validate_course(self, course):
        request = self.context["request"]
        teacher = request.user.teacher_profile
        if course.teacher_id != teacher.id:
            raise serializers.ValidationError("You can only upload results for your own courses.")
        return course

    def validate(self, attrs):
        course = attrs.get("course")
        student = attrs.get("student")
        marks_obtained = attrs.get("marks_obtained")
        total_marks = attrs.get("total_marks")

        if course and student and not student.courses.filter(id=course.id).exists():
            raise serializers.ValidationError(
                {"student": "This student is not enrolled in the selected course."}
            )
        if marks_obtained is not None and total_marks is not None and marks_obtained > total_marks:
            raise serializers.ValidationError(
                {"marks_obtained": "Marks obtained cannot exceed total marks."}
            )
        return attrs

    def create(self, validated_data):
        teacher = self.context["request"].user.teacher_profile
        validated_data["uploaded_by"] = teacher
        try:
            return Result.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "A result for this student, course, and exam type already exists. "
                "Update the existing record instead."
            )


class MyResultSerializer(serializers.ModelSerializer):
    """Read-only view for a student checking their own results."""

    course_code = serializers.CharField(source="course.code", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)
    percentage = serializers.ReadOnlyField()

    class Meta:
        model = Result
        fields = [
            "id", "course", "course_code", "course_name", "exam_type",
            "marks_obtained", "total_marks", "percentage", "remarks",
        ]
        read_only_fields = fields
