from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department, Course, Student, Attachment

User = get_user_model()

# ----------------------------
# User Serializer (Signup + Profile)
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_admin", "password"]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        # Ensure password is hashed
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ----------------------------
# Department Serializer
# ----------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


# ----------------------------
# Course Serializer
# ----------------------------
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


# ----------------------------
# Attachment Serializer
# ----------------------------



# ----------------------------
# Student Serializer
# ----------------------------


class AttachmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all()
    )
    
    birth_certificate_url = serializers.SerializerMethodField()
    form_four_certificate_url = serializers.SerializerMethodField()
    form_six_certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            'id',
            'student',
            'birth_certificate_url',
            'form_four_certificate_url',
            'form_six_certificate_url',
        ]

    def get_birth_certificate_url(self, obj):
        if obj.birth_certificate:
            return obj.birth_certificate.url
        return None

    def get_form_four_certificate_url(self, obj):
        if obj.form_four_certificate:
            return obj.form_four_certificate.url
        return None

    def get_form_six_certificate_url(self, obj):
        if obj.form_six_certificate:
            return obj.form_six_certificate.url
        return None


class StudentSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(required=False)
    photo_url = serializers.SerializerMethodField()  # Add photo URL

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "gender",
            "photo_url",  # use URL instead of raw CloudinaryField
            "registration_number",
            "course",
            "department",
            "attachments",
        ]
        read_only_fields = ["registration_number"]

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def create(self, validated_data):
        attachments_data = validated_data.pop("attachments", None)
        student = Student.objects.create(**validated_data)
        if attachments_data:
            Attachment.objects.create(student=student, **attachments_data)
        return student

    def update(self, instance, validated_data):
        attachments_data = validated_data.pop("attachments", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if attachments_data:
            # update existing attachment or create if not exist
            attachment, created = Attachment.objects.get_or_create(student=instance)
            for attr, value in attachments_data.items():
                setattr(attachment, attr, value)
            attachment.save()

        return instance