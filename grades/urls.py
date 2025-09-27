from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('my-grades/', views.student_grades_view, name='student_grades'),
    path('transcript/', views.transcript_view, name='transcript'),
    
    # Teacher URLs
    path('teacher/sections/', views.teacher_grading_sections_view, name='teacher_grading_sections'),
    path('teacher/section/<int:section_id>/grades/', views.grade_students_view, name='grade_students'),
    path('teacher/section/<int:section_id>/assignments/', views.grade_assignments_view, name='grade_assignments'),
    path('teacher/assignment/<int:assignment_id>/submissions/', views.assignment_submissions_view, name='assignment_submissions'),
]