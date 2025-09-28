#!/usr/bin/env python3
"""
Setup calendar demo data for CTA
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
django.setup()

from django.contrib.auth.models import User
from calendar_app.models import EventCategory, CalendarEvent, AcademicCalendar, PersonalReminder
from accounts.models import Profile, Student, Teacher
from courses.models import Section, Course, Assignment


def setup_calendar_data():
    print("Setting up calendar demo data...")
    
    # Create Event Categories
    categories_data = [
        {'name': 'Classes', 'color': '#007bff', 'icon': 'fas fa-chalkboard-teacher'},
        {'name': 'Assignments', 'color': '#ffc107', 'icon': 'fas fa-tasks'},
        {'name': 'Exams', 'color': '#dc3545', 'icon': 'fas fa-clipboard-check'},
        {'name': 'Holidays', 'color': '#28a745', 'icon': 'fas fa-calendar-day'},
        {'name': 'Meetings', 'color': '#6f42c1', 'icon': 'fas fa-users'},
        {'name': 'Deadlines', 'color': '#fd7e14', 'icon': 'fas fa-exclamation-triangle'},
    ]
    
    for cat_data in categories_data:
        category, created = EventCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✓ Created category: {category.name}")
    
    # Create Academic Calendar
    current_year = timezone.now().year
    academic_calendar, created = AcademicCalendar.objects.get_or_create(
        semester='fall',
        year=current_year,
        defaults={
            'name': f'Fall {current_year}',
            'start_date': datetime(current_year, 8, 15).date(),
            'end_date': datetime(current_year, 12, 15).date(),
            'registration_start': datetime(current_year, 7, 1).date(),
            'registration_end': datetime(current_year, 8, 10).date(),
            'classes_start': datetime(current_year, 8, 20).date(),
            'classes_end': datetime(current_year, 12, 10).date(),
            'midterm_start': datetime(current_year, 10, 15).date(),
            'midterm_end': datetime(current_year, 10, 25).date(),
            'final_exam_start': datetime(current_year, 12, 5).date(),
            'final_exam_end': datetime(current_year, 12, 15).date(),
            'is_current': True,
        }
    )
    if created:
        print(f"✓ Created academic calendar: {academic_calendar.name}")
    
    # Get categories
    class_category = EventCategory.objects.get(name='Classes')
    assignment_category = EventCategory.objects.get(name='Assignments')
    exam_category = EventCategory.objects.get(name='Exams')
    holiday_category = EventCategory.objects.get(name='Holidays')
    meeting_category = EventCategory.objects.get(name='Meetings')
    
    # Get users and sections for events
    try:
        admin_user = User.objects.get(username='admin')
        sections = Section.objects.all()[:3]  # Get first 3 sections
        
        # Create sample events
        now = timezone.now()
        events_data = [
            # Classes
            {
                'title': 'Database Systems Lecture',
                'description': 'Introduction to database design and SQL',
                'event_type': 'class',
                'category': class_category,
                'start_datetime': now.replace(hour=10, minute=0, second=0, microsecond=0),
                'end_datetime': now.replace(hour=11, minute=30, second=0, microsecond=0),
                'priority': 'medium',
                'is_public': True,
                'section': sections[0] if sections else None,
            },
            {
                'title': 'Programming Fundamentals Lab',
                'description': 'Hands-on programming exercises',
                'event_type': 'class',
                'category': class_category,
                'start_datetime': (now + timedelta(days=1)).replace(hour=14, minute=0, second=0, microsecond=0),
                'end_datetime': (now + timedelta(days=1)).replace(hour=16, minute=0, second=0, microsecond=0),
                'priority': 'medium',
                'is_public': True,
                'section': sections[1] if len(sections) > 1 else None,
            },
            
            # Assignments
            {
                'title': 'Database Design Assignment Due',
                'description': 'Submit your database schema design',
                'event_type': 'assignment',
                'category': assignment_category,
                'start_datetime': (now + timedelta(days=3)).replace(hour=23, minute=59, second=0, microsecond=0),
                'end_datetime': (now + timedelta(days=3)).replace(hour=23, minute=59, second=0, microsecond=0),
                'priority': 'high',
                'is_public': True,
                'all_day': True,
            },
            {
                'title': 'Programming Project Submission',
                'description': 'Final project for Programming Fundamentals',
                'event_type': 'assignment',
                'category': assignment_category,
                'start_datetime': (now + timedelta(days=7)).replace(hour=23, minute=59, second=0, microsecond=0),
                'end_datetime': (now + timedelta(days=7)).replace(hour=23, minute=59, second=0, microsecond=0),
                'priority': 'urgent',
                'is_public': True,
                'all_day': True,
            },
            
            # Exams
            {
                'title': 'Midterm Examination - Database Systems',
                'description': 'Comprehensive midterm covering chapters 1-6',
                'event_type': 'exam',
                'category': exam_category,
                'start_datetime': (now + timedelta(days=14)).replace(hour=9, minute=0, second=0, microsecond=0),
                'end_datetime': (now + timedelta(days=14)).replace(hour=12, minute=0, second=0, microsecond=0),
                'priority': 'urgent',
                'is_public': True,
                'section': sections[0] if sections else None,
            },
            
            # Academic Events
            {
                'title': 'Registration Opens for Spring Semester',
                'description': 'Online registration begins for all students',
                'event_type': 'registration',
                'category': meeting_category,
                'start_datetime': (now + timedelta(days=21)).replace(hour=8, minute=0, second=0, microsecond=0),
                'end_datetime': (now + timedelta(days=21)).replace(hour=17, minute=0, second=0, microsecond=0),
                'priority': 'high',
                'is_public': True,
                'all_day': True,
            },
            
            # Holidays
            {
                'title': 'Independence Day Holiday',
                'description': 'Ghana Independence Day - No classes',
                'event_type': 'holiday',
                'category': holiday_category,
                'start_datetime': datetime(2026, 3, 6).replace(tzinfo=timezone.get_current_timezone()),
                'end_datetime': datetime(2026, 3, 6).replace(tzinfo=timezone.get_current_timezone()),
                'priority': 'low',
                'is_public': True,
                'all_day': True,
            },
            
            # Meetings
            {
                'title': 'Faculty Senate Meeting',
                'description': 'Monthly faculty senate meeting',
                'event_type': 'meeting',
                'category': meeting_category,
                'start_datetime': (now + timedelta(days=10)).replace(hour=15, minute=0, second=0, microsecond=0),
                'end_datetime': (now + timedelta(days=10)).replace(hour=17, minute=0, second=0, microsecond=0),
                'priority': 'medium',
                'is_public': False,
            },
            
            # Orientation
            {
                'title': 'New Student Orientation',
                'description': 'Welcome session for new students',
                'event_type': 'orientation',
                'category': meeting_category,
                'start_datetime': (now + timedelta(days=30)).replace(hour=9, minute=0, second=0, microsecond=0),
                'end_datetime': (now + timedelta(days=30)).replace(hour=16, minute=0, second=0, microsecond=0),
                'priority': 'high',
                'is_public': True,
            },
        ]
        
        for event_data in events_data:
            event, created = CalendarEvent.objects.get_or_create(
                title=event_data['title'],
                start_datetime=event_data['start_datetime'],
                defaults={
                    **event_data,
                    'created_by': admin_user,
                }
            )
            if created:
                print(f"✓ Created event: {event.title}")
        
        # Create Personal Reminders for users
        users_with_profiles = User.objects.filter(profile__isnull=False)[:3]
        
        reminder_data = [
            {
                'title': 'Submit Assignment',
                'description': 'Don\'t forget to submit the database assignment',
                'reminder_type': 'assignment',
                'reminder_datetime': now + timedelta(days=2, hours=12),
                'notify_email': True,
            },
            {
                'title': 'Study for Midterm',
                'description': 'Start preparing for the database systems midterm',
                'reminder_type': 'exam',
                'reminder_datetime': now + timedelta(days=7),
                'notify_email': True,
            },
            {
                'title': 'Office Hours',
                'description': 'Visit professor for clarification on project',
                'reminder_type': 'meeting',
                'reminder_datetime': now + timedelta(days=1, hours=14),
                'notify_email': False,
            },
        ]
        
        for i, user in enumerate(users_with_profiles):
            if i < len(reminder_data):
                reminder_info = reminder_data[i]
                reminder, created = PersonalReminder.objects.get_or_create(
                    user=user,
                    title=reminder_info['title'],
                    reminder_datetime=reminder_info['reminder_datetime'],
                    defaults=reminder_info
                )
                if created:
                    print(f"✓ Created reminder for {user.username}: {reminder.title}")
        
    except User.DoesNotExist:
        print("⚠ Admin user not found. Please create admin user first.")
    except Exception as e:
        print(f"⚠ Error creating sample events: {str(e)}")
    
    print("\n📅 Calendar demo data setup complete!")
    print("You can now view the calendar at: /calendar/")


if __name__ == '__main__':
    setup_calendar_data()