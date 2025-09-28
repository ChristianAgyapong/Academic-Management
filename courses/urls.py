from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('enroll/<int:section_id>/', views.enroll_course_view, name='enroll_course'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
    path('section/<int:section_id>/', views.section_detail_view, name='section_detail'),
    
    # Course section-specific URLs
    path('section/<int:section_id>/overview/', views.section_overview_view, name='section_overview'),
    path('section/<int:section_id>/syllabus/', views.section_syllabus_view, name='section_syllabus'),
    path('section/<int:section_id>/lessons/', views.section_lessons_view, name='section_lessons'),
    path('section/<int:section_id>/calendar/', views.section_calendar_view, name='section_calendar'),
    path('section/<int:section_id>/announcements/', views.section_announcements_view, name='section_announcements'),
    path('section/<int:section_id>/resources/', views.section_resources_view, name='section_resources'),
    path('section/<int:section_id>/discussions/', views.section_discussions_view, name='section_discussions'),
    path('section/<int:section_id>/assignments/', views.section_assignments_view, name='section_assignments'),
    path('section/<int:section_id>/tests/', views.section_tests_view, name='section_tests'),
    path('section/<int:section_id>/gradebook/', views.section_gradebook_view, name='section_gradebook'),
    path('section/<int:section_id>/dropbox/', views.section_dropbox_view, name='section_dropbox'),
    path('section/<int:section_id>/chat/', views.section_chat_view, name='section_chat'),
    path('section/<int:section_id>/email/', views.section_email_view, name='section_email'),
    path('section/<int:section_id>/roster/', views.section_roster_view, name='section_roster'),
    path('section/<int:section_id>/help/', views.section_help_view, name='section_help'),
    
    # Legacy URLs for backward compatibility
    path('section/<int:section_id>/materials/', views.course_materials_view, name='course_materials'),
    path('section/<int:section_id>/assignments/', views.assignments_view, name='assignments'),
    
    # Teacher URLs
    path('teacher/sections/', views.teacher_sections_view, name='teacher_sections'),
    path('teacher/section/<int:section_id>/', views.teacher_section_detail_view, name='teacher_section_detail'),
    path('teacher/section/<int:section_id>/upload-material/', views.upload_material_view, name='upload_material'),
    path('teacher/section/<int:section_id>/create-assignment/', views.create_assignment_view, name='create_assignment'),
    path('teacher/section/<int:section_id>/analytics/', views.teacher_analytics_view, name='teacher_analytics'),
    path('teacher/section/<int:section_id>/settings/', views.teacher_section_settings_view, name='teacher_section_settings'),
    
    # Admin URLs
    path('admin/manage/', views.manage_courses_view, name='manage_courses'),
    path('admin/create-course/', views.create_course_view, name='create_course'),
    path('admin/create-section/', views.create_section_view, name='create_section'),
]