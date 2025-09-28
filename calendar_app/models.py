from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile, Student, Teacher
from courses.models import Section, Assignment
from django.utils import timezone


class EventCategory(models.Model):
    """Categories for calendar events"""
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    icon = models.CharField(max_length=50, default='fas fa-calendar')
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Event Categories"
    
    def __str__(self):
        return self.name


class CalendarEvent(models.Model):
    """Calendar events for the academic system"""
    EVENT_TYPES = [
        ('assignment', 'Assignment Due'),
        ('exam', 'Examination'),
        ('class', 'Class Session'),
        ('holiday', 'Holiday'),
        ('meeting', 'Meeting'),
        ('deadline', 'Deadline'),
        ('orientation', 'Orientation'),
        ('graduation', 'Graduation'),
        ('registration', 'Registration'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Related objects
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    
    # Participants
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    attendees = models.ManyToManyField(User, blank=True, related_name='calendar_events')
    
    # Settings
    is_public = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=100, blank=True)  # JSON or simple pattern
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_datetime']
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def duration_minutes(self):
        """Calculate event duration in minutes"""
        return (self.end_datetime - self.start_datetime).total_seconds() / 60
    
    @property
    def is_today(self):
        """Check if event is today"""
        return self.start_datetime.date() == timezone.now().date()
    
    @property
    def is_past(self):
        """Check if event has passed"""
        return self.end_datetime < timezone.now()
    
    @property
    def is_upcoming(self):
        """Check if event is upcoming (within next 7 days)"""
        seven_days = timezone.now() + timezone.timedelta(days=7)
        return self.start_datetime <= seven_days and not self.is_past


class AcademicCalendar(models.Model):
    """Academic calendar for semesters and important dates"""
    SEMESTER_CHOICES = [
        ('fall', 'Fall Semester'),
        ('spring', 'Spring Semester'),
        ('summer', 'Summer Semester'),
    ]
    
    name = models.CharField(max_length=100)  # e.g., "Fall 2025"
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    registration_start = models.DateField()
    registration_end = models.DateField()
    
    classes_start = models.DateField()
    classes_end = models.DateField()
    
    midterm_start = models.DateField(null=True, blank=True)
    midterm_end = models.DateField(null=True, blank=True)
    
    final_exam_start = models.DateField(null=True, blank=True)
    final_exam_end = models.DateField(null=True, blank=True)
    
    is_current = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-start_date']
        unique_together = ['semester', 'year']
    
    def __str__(self):
        return f"{self.name} ({self.year})"
    
    def save(self, *args, **kwargs):
        # Ensure only one current academic calendar
        if self.is_current:
            AcademicCalendar.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)


class PersonalReminder(models.Model):
    """Personal reminders for users"""
    REMINDER_TYPES = [
        ('assignment', 'Assignment Reminder'),
        ('exam', 'Exam Reminder'),
        ('meeting', 'Meeting Reminder'),
        ('personal', 'Personal Reminder'),
        ('deadline', 'Deadline Reminder'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES, default='personal')
    
    reminder_datetime = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    
    # Notification settings
    notify_email = models.BooleanField(default=False)
    notify_minutes_before = models.IntegerField(default=15)  # Minutes before to notify
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['reminder_datetime']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
