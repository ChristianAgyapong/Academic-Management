from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('enroll/<int:section_id>/', views.enroll_course_view, name='enroll_course'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
    path('section/<int:section_id>/', views.section_detail_view, name='section_detail'),
    path('section/<int:section_id>/materials/', views.course_materials_view, name='course_materials'),
    path('section/<int:section_id>/assignments/', views.assignments_view, name='assignments'),
    
    # Teacher URLs
    path('teacher/sections/', views.teacher_sections_view, name='teacher_sections'),
    path('teacher/section/<int:section_id>/', views.teacher_section_detail_view, name='teacher_section_detail'),
    path('teacher/section/<int:section_id>/upload-material/', views.upload_material_view, name='upload_material'),
    path('teacher/section/<int:section_id>/create-assignment/', views.create_assignment_view, name='create_assignment'),
    
    # Admin URLs
    path('admin/manage/', views.manage_courses_view, name='manage_courses'),
    path('admin/create-course/', views.create_course_view, name='create_course'),
    path('admin/create-section/', views.create_section_view, name='create_section'),
]