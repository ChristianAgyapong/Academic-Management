from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    TEACHER = 'teacher', 'Teacher'
    STUDENT = 'student', 'Student'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=UserRole.choices)
    phone_number = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        blank=True
    )
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(blank=True, help_text="Tell us about yourself")
    pronunciation_guide = models.CharField(max_length=200, blank=True, help_text="How to pronounce your name")
    preferred_pronouns = models.CharField(max_length=50, blank=True, help_text="e.g., he/him, she/her, they/them")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    admission_date = models.DateField()
    graduation_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    medical_conditions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student_id} - {self.profile.user.get_full_name()}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    join_date = models.DateField()
    is_active = models.BooleanField(default=True)
    specialization = models.CharField(max_length=200, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    research_interests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee_id} - {self.profile.user.get_full_name()}"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
