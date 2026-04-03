from django.contrib import admin
from django.utils.html import format_html
from .models import User, Department, Course, Student, Attachment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_admin", "is_staff", "is_superuser")
    search_fields = ("username", "email")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")
    search_fields = ("name", "faculty")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "credits", "department")
    search_fields = ("code", "name")

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number", "first_name", "last_name",
        "email", "phone_number", "course", "department", "photo_tag"
    )
    search_fields = ("registration_number", "first_name", "last_name", "email")

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:50px;width:50px;border-radius:5px;" />', obj.photo.url)
        return "No Photo"
    photo_tag.short_description = "Photo"

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "student", "birth_certificate",
        "form_four_certificate", "form_six_certificate", "uploaded_at"
    )
