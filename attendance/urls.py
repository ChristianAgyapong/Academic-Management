from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('my-attendance/', views.student_attendance_view, name='student_attendance'),
    path('section/<int:section_id>/attendance/', views.section_attendance_view, name='section_attendance'),
    
    # Teacher URLs
    path('teacher/sections/', views.teacher_attendance_sections_view, name='teacher_attendance_sections'),
    path('teacher/section/<int:section_id>/mark/', views.mark_attendance_view, name='mark_attendance'),
    path('teacher/section/<int:section_id>/history/', views.attendance_history_view, name='attendance_history'),
]