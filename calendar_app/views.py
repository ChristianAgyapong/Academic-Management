from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
import calendar as cal
import json

from .models import CalendarEvent, EventCategory, AcademicCalendar, PersonalReminder
from accounts.models import Profile
from courses.models import Assignment, Section


@login_required
def calendar_view(request):
    """Main calendar view"""
    # Get current date or requested date
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Create calendar
    cal_obj = cal.Calendar(firstweekday=6)  # Start week on Sunday
    month_days = cal_obj.monthdayscalendar(year, month)
    
    # Get events for the month
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
    
    # Filter events based on user role
    profile = get_object_or_404(Profile, user=request.user)
    events_query = CalendarEvent.objects.filter(
        start_datetime__date__range=[start_date, end_date]
    )
    
    if profile.role == 'student':
        # Students see their enrolled course events and public events
        from courses.models import Enrollment
        enrollments = Enrollment.objects.filter(student__profile=profile)
        sections = [e.section for e in enrollments]
        events_query = events_query.filter(
            Q(section__in=sections) | 
            Q(is_public=True) | 
            Q(attendees=request.user)
        )
    elif profile.role == 'teacher':
        # Teachers see their teaching sections and public events
        sections = Section.objects.filter(teacher__profile=profile)
        events_query = events_query.filter(
            Q(section__in=sections) | 
            Q(created_by=request.user) |
            Q(is_public=True) | 
            Q(attendees=request.user)
        )
    else:  # Admin
        # Admins see all events
        pass
    
    events = events_query.distinct()
    
    # Get reminders for the user
    reminders = PersonalReminder.objects.filter(
        user=request.user,
        reminder_datetime__date__range=[start_date, end_date],
        is_completed=False
    )
    
    # Get academic calendar
    academic_calendar = AcademicCalendar.objects.filter(is_current=True).first()
    
    # Prepare event data for JavaScript
    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_datetime.isoformat(),
            'end': event.end_datetime.isoformat(),
            'type': event.event_type,
            'priority': event.priority,
            'allDay': event.all_day,
            'color': event.category.color if event.category else '#007bff',
        })
    
    for reminder in reminders:
        events_data.append({
            'id': f'reminder_{reminder.id}',
            'title': f'📝 {reminder.title}',
            'start': reminder.reminder_datetime.isoformat(),
            'type': 'reminder',
            'priority': 'medium',
            'color': '#ffc107',
        })
    
    context = {
        'year': year,
        'month': month,
        'month_name': cal.month_name[month],
        'month_days': month_days,
        'events': events,
        'events_data': json.dumps(events_data),
        'reminders': reminders,
        'academic_calendar': academic_calendar,
        'profile': profile,
        'today': timezone.now().date(),
        
        # Navigation
        'prev_month': month - 1 if month > 1 else 12,
        'prev_year': year if month > 1 else year - 1,
        'next_month': month + 1 if month < 12 else 1,
        'next_year': year if month < 12 else year + 1,
    }
    
    return render(request, 'calendar_app/calendar.html', context)


@login_required
def event_detail_view(request, event_id):
    """View event details"""
    event = get_object_or_404(CalendarEvent, id=event_id)
    
    # Check permissions
    profile = get_object_or_404(Profile, user=request.user)
    if not event.is_public and event.created_by != request.user and request.user not in event.attendees.all():
        if profile.role == 'student':
            # Check if student is enrolled in the section
            if event.section:
                from courses.models import Enrollment
                if not Enrollment.objects.filter(student__profile=profile, section=event.section).exists():
                    messages.error(request, "You don't have permission to view this event.")
                    return redirect('calendar_app:calendar')
        elif profile.role == 'teacher':
            # Check if teacher teaches the section
            if event.section and event.section.teacher.profile != profile:
                messages.error(request, "You don't have permission to view this event.")
                return redirect('calendar_app:calendar')
    
    context = {
        'event': event,
        'profile': profile,
    }
    
    return render(request, 'calendar_app/event_detail.html', context)


@login_required
def create_event_view(request):
    """Create a new calendar event - Only teachers and admins allowed"""
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check if user has permission to create events
    if profile.role == 'student':
        messages.error(request, "Students are not allowed to create events. Please contact your teacher or administrator.")
        return redirect('calendar_app:calendar')
    
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            event_type = request.POST.get('event_type')
            start_datetime = request.POST.get('start_datetime')
            end_datetime = request.POST.get('end_datetime')
            all_day = request.POST.get('all_day') == 'on'
            priority = request.POST.get('priority', 'medium')
            is_public = request.POST.get('is_public') == 'on'
            section_id = request.POST.get('section')
            
            # Convert datetime strings
            start_dt = datetime.fromisoformat(start_datetime.replace('T', ' '))
            end_dt = datetime.fromisoformat(end_datetime.replace('T', ' '))
            
            # Create event
            event = CalendarEvent.objects.create(
                title=title,
                description=description,
                event_type=event_type,
                start_datetime=start_dt,
                end_datetime=end_dt,
                all_day=all_day,
                priority=priority,
                is_public=is_public,
                created_by=request.user,
                section_id=section_id if section_id else None,
            )
            
            messages.success(request, f'Event "{title}" created successfully!')
            return redirect('calendar_app:calendar')
            
        except Exception as e:
            messages.error(request, f'Error creating event: {str(e)}')
    
    # Get user's sections for dropdown
    sections = []
    if profile.role == 'teacher':
        sections = Section.objects.filter(teacher__profile=profile)
    elif profile.role == 'admin':
        sections = Section.objects.all()
    
    context = {
        'profile': profile,
        'sections': sections,
        'event_types': CalendarEvent.EVENT_TYPES,
        'priority_choices': CalendarEvent.PRIORITY_CHOICES,
    }
    
    return render(request, 'calendar_app/create_event.html', context)


@login_required
def events_api(request):
    """API endpoint for calendar events (AJAX)"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    if not start or not end:
        return JsonResponse({'events': []})
    
    try:
        start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
        
        profile = get_object_or_404(Profile, user=request.user)
        events_query = CalendarEvent.objects.filter(
            start_datetime__range=[start_date, end_date]
        )
        
        # Filter based on user role (same logic as calendar_view)
        if profile.role == 'student':
            from courses.models import Enrollment
            enrollments = Enrollment.objects.filter(student__profile=profile)
            sections = [e.section for e in enrollments]
            events_query = events_query.filter(
                Q(section__in=sections) | 
                Q(is_public=True) | 
                Q(attendees=request.user)
            )
        elif profile.role == 'teacher':
            sections = Section.objects.filter(teacher__profile=profile)
            events_query = events_query.filter(
                Q(section__in=sections) | 
                Q(created_by=request.user) |
                Q(is_public=True) | 
                Q(attendees=request.user)
            )
        
        events = events_query.distinct()
        
        events_data = []
        for event in events:
            events_data.append({
                'id': event.id,
                'title': event.title,
                'start': event.start_datetime.isoformat(),
                'end': event.end_datetime.isoformat(),
                'allDay': event.all_day,
                'backgroundColor': event.category.color if event.category else '#007bff',
                'borderColor': event.category.color if event.category else '#007bff',
                'textColor': '#ffffff',
                'extendedProps': {
                    'description': event.description,
                    'type': event.event_type,
                    'priority': event.priority,
                }
            })
        
        return JsonResponse(events_data, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
