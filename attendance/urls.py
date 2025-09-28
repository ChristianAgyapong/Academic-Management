from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Student URLs
    path('my-attendance/', views.student_attendance_view, name='student_attendance'),
    
    # Teacher URLs
    path('teacher/sections/', views.teacher_attendance_sections_view, name='teacher_attendance_sections'),
    path('teacher/reports/', views.attendance_reports_view, name='attendance_reports'),
    
    # Section-specific URLs
    path('section/<int:section_id>/', views.section_attendance_view, name='section_attendance'),
    path('section/<int:section_id>/mark/', views.mark_attendance_view, name='mark_attendance'),
    path('section/<int:section_id>/history/', views.attendance_history_view, name='attendance_history'),
    path('section/<int:section_id>/export/', views.export_attendance_csv, name='export_attendance'),
]