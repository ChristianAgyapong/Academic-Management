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
    """Student section detail view with course materials, assignments, and info"""
    from django.utils import timezone
    from grades.models import Grade
    from attendance.models import Attendance, AttendanceSession
    
    section = get_object_or_404(Section, id=section_id)
    
    # Check if user is enrolled in this section
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get course materials
    materials = Material.objects.filter(
        section=section, 
        is_visible=True
    ).order_by('-upload_date')
    
    # Get assignments
    assignments = Assignment.objects.filter(
        section=section
    ).order_by('due_date')
    
    # Get enrollment count
    enrollment_count = Enrollment.objects.filter(
        section=section, 
        status='enrolled'
    ).count()
    
    # Get student's attendance rate (if student)
    attendance_rate = 0
    if profile.role == 'student':
        total_sessions = AttendanceSession.objects.filter(
            section=section
        ).count()
        
        if total_sessions > 0:
            attended_sessions = Attendance.objects.filter(
                session__section=section,
                student__profile=profile,
                status__in=['present', 'late']  # Count both present and late as attended
            ).count()
            attendance_rate = round((attended_sessions / total_sessions) * 100, 1)
    
    context = {
        'section': section,
        'materials': materials,
        'assignments': assignments,
        'enrollment_count': enrollment_count,
        'materials_count': materials.count(),
        'assignments_count': assignments.count(),
        'attendance_rate': attendance_rate,
        'today': timezone.now().date(),
        'profile': profile,
    }
    
    # Redirect to the clean overview page instead of the old section_detail template
    return redirect('courses:section_overview', section_id=section_id)

# ==================== SECTION-SPECIFIC VIEWS ====================

@login_required
def section_overview_view(request, section_id):
    """Main overview page for a course section"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get course statistics
    enrollments = Enrollment.objects.filter(section=section)
    total_students = enrollments.count()
    total_assignments = 8  # Sample data
    total_announcements = 12  # Sample data
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Overview',
        'page_description': 'Course information and recent activity',
        'total_students': total_students,
        'total_assignments': total_assignments,
        'total_announcements': total_announcements,
    }
    
    return render(request, 'courses/section_overview.html', context)

@login_required
def section_syllabus_view(request, section_id):
    """Course syllabus and curriculum view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get course materials organized by type
    materials = Material.objects.filter(
        section=section, 
        is_visible=True
    ).order_by('-upload_date')
    
    context = {
        'section': section,
        'materials': materials,
        'profile': profile,
        'page_title': 'Syllabus',
    }
    
    return render(request, 'courses/section_syllabus.html', context)

@login_required
def section_lessons_view(request, section_id):
    """Course lessons and lecture materials view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get course materials (lessons)
    lessons = Material.objects.filter(
        section=section, 
        is_visible=True
    ).order_by('upload_date')
    
    context = {
        'section': section,
        'lessons': lessons,
        'profile': profile,
        'page_title': 'Lessons',
    }
    
    return render(request, 'courses/section_lessons.html', context)

@login_required
def section_calendar_view(request, section_id):
    """Course calendar and schedule view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get assignments for calendar
    assignments = Assignment.objects.filter(
        section=section
    ).order_by('due_date')
    
    context = {
        'section': section,
        'assignments': assignments,
        'profile': profile,
        'page_title': 'Calendar',
    }
    
    return render(request, 'courses/section_calendar.html', context)

@login_required
def section_announcements_view(request, section_id):
    """Course announcements view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Announcements',
    }
    
    return render(request, 'courses/section_announcements.html', context)

@login_required
def section_resources_view(request, section_id):
    """Course resources and materials view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get course materials
    materials = Material.objects.filter(
        section=section, 
        is_visible=True
    ).order_by('-upload_date')
    
    context = {
        'section': section,
        'materials': materials,
        'profile': profile,
        'page_title': 'Resources',
    }
    
    return render(request, 'courses/section_resources.html', context)

@login_required
def section_discussions_view(request, section_id):
    """Course discussions and forums view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Discussions',
    }
    
    return render(request, 'courses/section_discussions.html', context)

@login_required
def section_assignments_view(request, section_id):
    """Course assignments view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get assignments
    assignments = Assignment.objects.filter(
        section=section
    ).order_by('due_date')
    
    context = {
        'section': section,
        'assignments': assignments,
        'profile': profile,
        'today': timezone.now().date(),
        'page_title': 'Assignments',
    }
    
    return render(request, 'courses/section_assignments.html', context)

@login_required
def section_tests_view(request, section_id):
    """Course tests and quizzes view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Tests & Quizzes',
    }
    
    return render(request, 'courses/section_tests.html', context)

@login_required
def section_gradebook_view(request, section_id):
    """Course gradebook view"""
    from django.utils import timezone
    from grades.models import Grade
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get student grades
    grades = []
    if profile.role == 'student':
        grades = Grade.objects.filter(
            student__profile=profile,
            assignment__section=section
        ).select_related('assignment').order_by('-assignment__due_date')
    
    # Get assignments for this section
    assignments = Assignment.objects.filter(
        section=section
    ).order_by('due_date')
    
    context = {
        'section': section,
        'grades': grades,
        'assignments': assignments,
        'profile': profile,
        'page_title': 'Gradebook',
    }
    
    return render(request, 'courses/section_gradebook.html', context)

@login_required
def section_dropbox_view(request, section_id):
    """Course dropbox for file submissions view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Drop Box',
    }
    
    return render(request, 'courses/section_dropbox.html', context)

@login_required
def section_chat_view(request, section_id):
    """Course chat room view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Chat Room',
    }
    
    return render(request, 'courses/section_chat.html', context)

@login_required
def section_email_view(request, section_id):
    """Course email archive view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Email Archive',
    }
    
    return render(request, 'courses/section_email.html', context)

@login_required
def section_roster_view(request, section_id):
    """Course roster view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment or teacher access
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    # Get enrolled students for the roster
    enrollments = Enrollment.objects.filter(section=section).select_related('student__profile__user')
    total_students = enrollments.count()
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Class Roster',
        'enrollments': enrollments,
        'total_students': total_students,
    }
    
    return render(request, 'courses/section_roster.html', context)

@login_required
def section_help_view(request, section_id):
    """Course help view"""
    from django.utils import timezone
    
    section = get_object_or_404(Section, id=section_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check enrollment
    if profile.role == 'student':
        enrollment = Enrollment.objects.filter(
            student__profile=profile, 
            section=section
        ).first()
        if not enrollment:
            messages.error(request, "You are not enrolled in this section.")
            return redirect('accounts:dashboard')
    
    context = {
        'section': section,
        'profile': profile,
        'page_title': 'Help & Support',
    }
    
    return render(request, 'courses/section_help.html', context)

# ==================== LEGACY VIEWS ====================

@login_required
def course_materials_view(request, section_id):
    # Redirect to new resources view
    return redirect('courses:section_resources', section_id=section_id)

@login_required
def assignments_view(request, section_id):
    # Redirect to new assignments view
    return redirect('courses:section_assignments', section_id=section_id)

@login_required
def teacher_sections_view(request):
    # Placeholder - implement teacher sections view
    return render(request, 'courses/teacher_sections.html', {})

@login_required
def teacher_section_detail_view(request, section_id):
    # Get section and verify teacher access
    section = get_object_or_404(Section, id=section_id)
    
    # Verify the logged-in user is the teacher for this section
    if not hasattr(request.user, 'profile') or not hasattr(request.user.profile, 'teacher'):
        messages.error(request, 'Access denied. Teacher access required.')
        return redirect('accounts:dashboard')
    
    teacher = request.user.profile.teacher
    if section.teacher != teacher:
        messages.error(request, 'Access denied. You can only view your own sections.')
        return redirect('courses:teacher_sections')
    
    # Get enrolled students
    enrollments = Enrollment.objects.filter(section=section, status='enrolled').order_by('student__profile__user__first_name')
    
    context = {
        'section': section,
        'enrollments': enrollments,
        'teacher': teacher,
    }
    
    return render(request, 'courses/teacher_section_detail.html', context)

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

@login_required
def teacher_analytics_view(request, section_id):
    """Analytics view for teachers to see class performance"""
    section = get_object_or_404(Section, id=section_id)
    
    # Only teachers can view analytics for their sections
    if not (request.user.profile.role == UserRole.TEACHER and section.teacher.profile.user == request.user):
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    messages.success(request, f'Analytics for {section.course.code} - Section {section.section_number}')
    return redirect('courses:teacher_section_detail', section_id=section_id)

@login_required
def teacher_section_settings_view(request, section_id):
    """Settings view for teachers to manage section preferences"""
    section = get_object_or_404(Section, id=section_id)
    
    # Only teachers can view settings for their sections
    if not (request.user.profile.role == UserRole.TEACHER and section.teacher.profile.user == request.user):
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    messages.success(request, f'Settings for {section.course.code} - Section {section.section_number}')
    return redirect('courses:teacher_section_detail', section_id=section_id)
