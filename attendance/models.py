from django.db import models
from accounts.models import Student
from courses.models import Section

# Create your models here.

class AttendanceSession(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    topic_covered = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.section} - {self.date}"

    class Meta:
        verbose_name = "Attendance Session"
        verbose_name_plural = "Attendance Sessions"
        unique_together = ['section', 'date', 'start_time']

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    arrival_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    marked_by = models.CharField(max_length=100)  # Teacher who marked the attendance
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.session} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        unique_together = ['student', 'session']

class AttendanceSummary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    total_sessions = models.PositiveIntegerField(default=0)
    present_count = models.PositiveIntegerField(default=0)
    absent_count = models.PositiveIntegerField(default=0)
    late_count = models.PositiveIntegerField(default=0)
    excused_count = models.PositiveIntegerField(default=0)
    attendance_percentage = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.profile.user.username} - {self.section} - {self.attendance_percentage}%"

    def update_summary(self):
        """Calculate and update attendance summary"""
        attendance_records = Attendance.objects.filter(
            student=self.student,
            session__section=self.section
        )
        
        self.total_sessions = attendance_records.count()
        self.present_count = attendance_records.filter(status='present').count()
        self.absent_count = attendance_records.filter(status='absent').count()
        self.late_count = attendance_records.filter(status='late').count()
        self.excused_count = attendance_records.filter(status='excused').count()
        
        if self.total_sessions > 0:
            # Consider present and late as attended
            attended = self.present_count + self.late_count
            self.attendance_percentage = (attended / self.total_sessions) * 100
        else:
            self.attendance_percentage = 0.0
        
        self.save()

    class Meta:
        verbose_name = "Attendance Summary"
        verbose_name_plural = "Attendance Summaries"
        unique_together = ['student', 'section']
