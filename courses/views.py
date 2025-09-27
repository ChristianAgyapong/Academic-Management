from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Section, Enrollment, Material, Assignment
from accounts.models import Profile, Student, Teacher, UserRole

# Create your views here.

@login_required
def course_list_view(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def enroll_course_view(request, section_id):
    # Placeholder - implement enrollment logic
    messages.info(request, 'Enrollment feature coming soon!')
    return redirect('courses:course_list')

@login_required
def my_courses_view(request):
    # Placeholder - implement student course view
    return render(request, 'courses/my_courses.html', {})

@login_required
def section_detail_view(request, section_id):
    # Placeholder - implement section detail view
    section = get_object_or_404(Section, id=section_id)
    return render(request, 'courses/section_detail.html', {'section': section})

@login_required
def course_materials_view(request, section_id):
    # Placeholder - implement course materials view
    return render(request, 'courses/materials.html', {})

@login_required
def assignments_view(request, section_id):
    # Placeholder - implement assignments view
    return render(request, 'courses/assignments.html', {})

@login_required
def teacher_sections_view(request):
    # Placeholder - implement teacher sections view
    return render(request, 'courses/teacher_sections.html', {})

@login_required
def teacher_section_detail_view(request, section_id):
    # Placeholder - implement teacher section detail view
    return render(request, 'courses/teacher_section_detail.html', {})

@login_required
def upload_material_view(request, section_id):
    # Placeholder - implement material upload
    messages.info(request, 'Material upload feature coming soon!')
    return redirect('courses:teacher_sections')

@login_required
def create_assignment_view(request, section_id):
    # Placeholder - implement assignment creation
    messages.info(request, 'Assignment creation feature coming soon!')
    return redirect('courses:teacher_sections')

@login_required
def manage_courses_view(request):
    # Placeholder - implement course management
    return render(request, 'courses/manage_courses.html', {})

@login_required
def create_course_view(request):
    # Placeholder - implement course creation
    messages.info(request, 'Course creation feature coming soon!')
    return redirect('courses:manage_courses')

@login_required
def create_section_view(request):
    # Placeholder - implement section creation
    messages.info(request, 'Section creation feature coming soon!')
    return redirect('courses:manage_courses')
