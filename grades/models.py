from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Student
from courses.models import Section, Assignment

# Create your models here.

class GradeComponent(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Midterm Exam", "Final Exam", "Homework"
    weight_percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_points = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.name} - {self.section}"

    class Meta:
        verbose_name = "Grade Component"
        verbose_name_plural = "Grade Components"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    component = models.ForeignKey(GradeComponent, on_delete=models.CASCADE)
    points_earned = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    date_recorded = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.component.name}"

    @property
    def percentage(self):
        if self.component.max_points > 0:
            return (self.points_earned / self.component.max_points) * 100
        return 0

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        unique_together = ['student', 'component']

class AssignmentSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', blank=True)
    comments = models.TextField(blank=True)
    points_earned = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
    )
    is_graded = models.BooleanField(default=False)
    graded_date = models.DateTimeField(null=True, blank=True)
    teacher_comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.assignment.title}"

    @property
    def is_late(self):
        return self.submission_date > self.assignment.due_date

    @property
    def percentage(self):
        if self.points_earned and self.assignment.max_points > 0:
            return (self.points_earned / self.assignment.max_points) * 100
        return 0

    class Meta:
        verbose_name = "Assignment Submission"
        verbose_name_plural = "Assignment Submissions"
        unique_together = ['student', 'assignment']

class FinalGrade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (95-100)'),
        ('A', 'A (90-94)'),
        ('A-', 'A- (85-89)'),
        ('B+', 'B+ (80-84)'),
        ('B', 'B (75-79)'),
        ('B-', 'B- (70-74)'),
        ('C+', 'C+ (65-69)'),
        ('C', 'C (60-64)'),
        ('C-', 'C- (55-59)'),
        ('D', 'D (50-54)'),
        ('F', 'F (Below 50)'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    numerical_grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    letter_grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    gpa_points = models.FloatField()
    date_recorded = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.section} - {self.letter_grade}"

    def save(self, *args, **kwargs):
        # Auto-calculate letter grade and GPA points based on numerical grade
        if self.numerical_grade >= 95:
            self.letter_grade = 'A+'
            self.gpa_points = 4.0
        elif self.numerical_grade >= 90:
            self.letter_grade = 'A'
            self.gpa_points = 4.0
        elif self.numerical_grade >= 85:
            self.letter_grade = 'A-'
            self.gpa_points = 3.7
        elif self.numerical_grade >= 80:
            self.letter_grade = 'B+'
            self.gpa_points = 3.3
        elif self.numerical_grade >= 75:
            self.letter_grade = 'B'
            self.gpa_points = 3.0
        elif self.numerical_grade >= 70:
            self.letter_grade = 'B-'
            self.gpa_points = 2.7
        elif self.numerical_grade >= 65:
            self.letter_grade = 'C+'
            self.gpa_points = 2.3
        elif self.numerical_grade >= 60:
            self.letter_grade = 'C'
            self.gpa_points = 2.0
        elif self.numerical_grade >= 55:
            self.letter_grade = 'C-'
            self.gpa_points = 1.7
        elif self.numerical_grade >= 50:
            self.letter_grade = 'D'
            self.gpa_points = 1.0
        else:
            self.letter_grade = 'F'
            self.gpa_points = 0.0
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Final Grade"
        verbose_name_plural = "Final Grades"
        unique_together = ['student', 'section']
