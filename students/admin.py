from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "user", "department", "semester")
    search_fields = ("roll_number", "user__username", "user__email")
    list_filter = ("department", "semester")
    filter_horizontal = ("courses",)
