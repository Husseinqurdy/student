from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils import timezone

# ----------------------------
# Custom User (Admin/Staff)
# ----------------------------

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        # remove default validators so spaces and special chars are allowed
        validators=[],
    )
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username



# ----------------------------
# Department Model
# ----------------------------
class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    faculty = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# ----------------------------
# Course Model
# ----------------------------
class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.code} - {self.name}"


# ----------------------------
# Student Model
# ----------------------------
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    photo = CloudinaryField('students/photos/', blank=True, null=True)  # Cloudinary will handle storage
    registration_number = models.CharField(max_length=20, unique=True, editable=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="students")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="students")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.registration_number:
            prefix = "STU"
            year = timezone.now().year
            last_id = Student.objects.count() + 1
            self.registration_number = f"{prefix}{year}{last_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"


# ----------------------------
# Attachments Model
# ----------------------------
class Attachment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="attachments")
    birth_certificate = models.FileField(upload_to='students/attachments/', null=True, blank=True)
    form_four_certificate = models.FileField(upload_to='students/attachments/', null=True, blank=True)
    form_six_certificate = models.FileField(upload_to='students/attachments/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachments for {self.student.registration_number}"
