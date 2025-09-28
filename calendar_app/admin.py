from django.contrib import admin
from .models import EventCategory, CalendarEvent, AcademicCalendar, PersonalReminder


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'icon']
    list_editable = ['color', 'icon']
    search_fields = ['name']


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_datetime', 'end_datetime', 'priority', 'created_by', 'is_public']
    list_filter = ['event_type', 'priority', 'is_public', 'all_day', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_datetime'
    filter_horizontal = ['attendees']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'event_type', 'category')
        }),
        ('Date & Time', {
            'fields': ('start_datetime', 'end_datetime', 'all_day')
        }),
        ('Settings', {
            'fields': ('priority', 'is_public', 'is_recurring', 'recurrence_pattern')
        }),
        ('Relationships', {
            'fields': ('section', 'assignment', 'created_by', 'attendees')
        }),
    )


@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'semester', 'year', 'start_date', 'end_date', 'is_current']
    list_filter = ['semester', 'year', 'is_current']
    search_fields = ['name']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'semester', 'year', 'is_current')
        }),
        ('Academic Dates', {
            'fields': ('start_date', 'end_date', 'classes_start', 'classes_end')
        }),
        ('Registration Period', {
            'fields': ('registration_start', 'registration_end')
        }),
        ('Examination Periods', {
            'fields': ('midterm_start', 'midterm_end', 'final_exam_start', 'final_exam_end')
        }),
    )


@admin.register(PersonalReminder)
class PersonalReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'reminder_datetime', 'reminder_type', 'is_completed']
    list_filter = ['reminder_type', 'is_completed', 'notify_email']
    search_fields = ['title', 'user__username']
    date_hierarchy = 'reminder_datetime'
