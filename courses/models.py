from django.db import models
from accounts.models import Student, Teacher

# Create your models here.

class AcademicYear(models.Model):
    name = models.CharField(max_length=50)  # e.g., "2023-2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"

class Semester(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Fall 2023", "Spring 2024"
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField()
    department = models.CharField(max_length=100)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=10)
    max_capacity = models.PositiveIntegerField(default=30)
    schedule = models.TextField()  # Day and time information
    classroom = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.course.code} - Section {self.section_number}"

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        unique_together = ['course', 'semester', 'section_number']

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('enrolled', 'Enrolled'),
            ('dropped', 'Dropped'),
            ('completed', 'Completed')
        ],
        default='enrolled'
    )

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.section}"

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        unique_together = ['student', 'section']

class Material(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.section}"

    class Meta:
        verbose_name = "Course Material"
        verbose_name_plural = "Course Materials"

class Assignment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_points = models.PositiveIntegerField(default=100)
    file = models.FileField(upload_to='assignments/', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.section}"

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
