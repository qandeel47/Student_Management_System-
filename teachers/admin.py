from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "user", "department", "designation")
    search_fields = ("employee_id", "user__username", "user__email")
    list_filter = ("department",)
