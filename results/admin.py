from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "exam_type", "marks_obtained", "total_marks", "uploaded_by")
    list_filter = ("exam_type", "course")
    search_fields = ("student__roll_number",)
