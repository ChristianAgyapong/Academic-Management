from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from .models import Profile, Student, Teacher, UserRole
from .forms import (
    LoginForm, StudentRegistrationForm, TeacherRegistrationForm, ProfileUpdateForm, 
    ForgotPasswordForm, ResetPasswordForm, BasicInformationForm, NamePronunciationForm,
    ContactInformationForm, StudentInformationForm, StaffInformationForm, ProfilePictureForm
)
from courses.models import Enrollment, Section
from grades.models import FinalGrade
from attendance.models import AttendanceSummary
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
import uuid

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['username']  # This is actually student_id or employee_id
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            
            # Find user by Student ID or Employee ID
            user = None
            try:
                if user_type == 'student':
                    # Find student by student_id
                    student = Student.objects.get(student_id=id_number)
                    username = student.profile.user.username
                else:
                    # Find teacher by employee_id
                    teacher = Teacher.objects.get(employee_id=id_number)
                    username = teacher.profile.user.username
                
                # Authenticate using the found username
                user = authenticate(request, username=username, password=password)
            except (Student.DoesNotExist, Teacher.DoesNotExist):
                user = None
            
            if user is not None:
                # Check if user has a profile
                try:
                    profile = user.profile
                    
                    # Validate user type against profile role
                    if user_type == 'student' and profile.role != UserRole.STUDENT:
                        messages.error(request, 'Invalid credentials for student login')
                        return render(request, 'accounts/login.html', {'form': form})
                    elif user_type == 'staff' and profile.role not in [UserRole.TEACHER, UserRole.ADMIN]:
                        messages.error(request, 'Invalid credentials for staff login')
                        return render(request, 'accounts/login.html', {'form': form})
                    
                    # Login successful
                    login(request, user)
                    
                    # Show welcome message based on role
                    if profile.role == UserRole.ADMIN:
                        messages.success(request, f'Welcome Admin, {user.get_full_name() or username}!')
                    elif profile.role == UserRole.TEACHER:
                        messages.success(request, f'Welcome Teacher, {user.get_full_name() or username}!')
                    elif profile.role == UserRole.STUDENT:
                        messages.success(request, f'Welcome Student, {user.get_full_name() or username}!')
                    
                    return redirect('accounts:dashboard')
                    
                except Profile.DoesNotExist:
                    messages.error(request, 'User profile not found. Please contact administrator.')
            else:
                # Customize error message based on user type
                if user_type == 'student':
                    messages.error(request, 'Invalid Student ID or Password')
                else:
                    messages.error(request, 'Invalid Employee ID or Password')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    from courses.models import Enrollment, Section, Course, Assignment
    from grades.models import Grade, FinalGrade
    from attendance.models import Attendance, AttendanceSession
    from django.db.models import Avg, Count
    from datetime import datetime, timedelta
    
    profile = get_object_or_404(Profile, user=request.user)
    
    # Base context for all users
    context = {
        'profile': profile,
        'current_date': datetime.now(),
        'recent_activities': [],
    }
    
    # Generate sample recent activities based on user role
    if profile.role == UserRole.ADMIN:
        # Admin dashboard data
        total_students = Student.objects.filter(is_active=True).count()
        total_teachers = Teacher.objects.filter(is_active=True).count()
        total_courses = Course.objects.filter(is_active=True).count()
        active_enrollments = Enrollment.objects.filter(status='enrolled').count()
        
        context.update({
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'active_enrollments': active_enrollments,
            'recent_activities': [
                {
                    'title': 'New Student Registered',
                    'description': f'Total students: {total_students}',
                    'icon': 'fas fa-user-plus',
                    'date': datetime.now() - timedelta(hours=2)
                },
                {
                    'title': 'System Backup Completed',
                    'description': 'Daily backup completed successfully',
                    'icon': 'fas fa-database',
                    'date': datetime.now() - timedelta(hours=8)
                },
                {
                    'title': 'Course Enrollment Updated',
                    'description': f'{active_enrollments} active enrollments',
                    'icon': 'fas fa-book',
                    'date': datetime.now() - timedelta(days=1)
                }
            ]
        })
    
    elif profile.role == UserRole.TEACHER:
        try:
            teacher = Teacher.objects.get(profile=profile)
            sections = Section.objects.filter(teacher=teacher)
            
            # Count total students across all sections
            total_students = Enrollment.objects.filter(
                section__in=sections, 
                status='enrolled'
            ).count()
            
            # Count assignments
            assignments_count = Assignment.objects.filter(section__in=sections).count()
            
            # Placeholder for pending grades (assignments without grades)
            pending_grades = assignments_count  # Simplified
            
            context.update({
                'teacher': teacher,
                'sections': sections,
                'sections_count': sections.count(),
                'students_count': total_students,
                'assignments_count': assignments_count,
                'pending_grades': pending_grades,
                'recent_activities': [
                    {
                        'title': 'Attendance Recorded',
                        'description': f'Marked attendance for {sections.count()} sections',
                        'icon': 'fas fa-calendar-check',
                        'date': datetime.now() - timedelta(hours=1)
                    },
                    {
                        'title': 'Grades Updated',
                        'description': f'Updated grades for {total_students} students',
                        'icon': 'fas fa-chart-line',
                        'date': datetime.now() - timedelta(hours=4)
                    },
                    {
                        'title': 'New Assignment Posted',
                        'description': f'Posted new assignment in CS101',
                        'icon': 'fas fa-tasks',
                        'date': datetime.now() - timedelta(days=1)
                    }
                ]
            })
        except Teacher.DoesNotExist:
            context.update({
                'sections_count': 0,
                'students_count': 0,
                'assignments_count': 0,
                'pending_grades': 0
            })
    
    elif profile.role == UserRole.STUDENT:
        try:
            student = Student.objects.get(profile=profile)
            enrollments = Enrollment.objects.filter(student=student, status='enrolled')
            recent_grades = FinalGrade.objects.filter(student=student).order_by('-date_recorded')[:5]
            
            # Calculate average grade from component grades
            grades = Grade.objects.filter(student=student)
            if grades.exists():
                avg_grade = grades.aggregate(avg=Avg('points_earned'))['avg']
                context['avg_grade'] = avg_grade or 0
            else:
                context['avg_grade'] = 0
            
            # Calculate attendance rate
            attendances = Attendance.objects.filter(student=student)
            if attendances.exists():
                present_count = attendances.filter(status__in=['present', 'late']).count()
                total_count = attendances.count()
                context['attendance_rate'] = (present_count / total_count * 100) if total_count > 0 else 0
            else:
                context['attendance_rate'] = 0
            
            # Count pending assignments (simplified)
            pending_assignments = Assignment.objects.filter(
                section__in=enrollments.values_list('section', flat=True),
                due_date__gt=datetime.now()
            ).count()
            
            context.update({
                'student': student,
                'enrollments': enrollments,
                'recent_grades': recent_grades,
                'enrollments_count': enrollments.count(),
                'pending_assignments': pending_assignments,
                'recent_activities': [
                    {
                        'title': 'Grade Posted',
                        'description': f'New grade available for {enrollments.first().section.course.name if enrollments.exists() else "course"}',
                        'icon': 'fas fa-star',
                        'date': datetime.now() - timedelta(hours=3)
                    },
                    {
                        'title': 'Assignment Submitted',
                        'description': 'Successfully submitted assignment',
                        'icon': 'fas fa-check-circle',
                        'date': datetime.now() - timedelta(hours=6)
                    },
                    {
                        'title': 'Class Attendance',
                        'description': f'Attended {enrollments.count()} classes today',
                        'icon': 'fas fa-calendar-check',
                        'date': datetime.now() - timedelta(days=1)
                    }
                ]
            })
        except Student.DoesNotExist:
            context.update({
                'enrollments_count': 0,
                'avg_grade': 0,
                'attendance_rate': 0,
                'pending_assignments': 0
            })
    
    return render(request, 'accounts/dashboard_home.html', context)

@login_required
def profile_view(request):
    from courses.models import Enrollment, Section
    from grades.models import Grade
    from attendance.models import Attendance
    from django.db.models import Avg, Count
    
    profile = get_object_or_404(Profile, user=request.user)
    context = {'profile': profile}
    
    # Add statistics based on user role
    if profile.role == 'student':
        try:
            student = profile.student
            enrollments = Enrollment.objects.filter(student=student, status='enrolled')
            context['enrollments_count'] = enrollments.count()
            
            # Calculate average grade
            grades = Grade.objects.filter(student=student)
            if grades.exists():
                avg_grade = grades.aggregate(avg=Avg('points_earned'))['avg']
                context['avg_grade'] = avg_grade or 0
            else:
                context['avg_grade'] = 0
            
            # Calculate attendance rate
            attendances = Attendance.objects.filter(student=student)
            if attendances.exists():
                present_count = attendances.filter(status__in=['present', 'late']).count()
                total_count = attendances.count()
                context['attendance_rate'] = (present_count / total_count * 100) if total_count > 0 else 0
            else:
                context['attendance_rate'] = 0
                
        except:
            context.update({
                'enrollments_count': 0,
                'avg_grade': 0,
                'attendance_rate': 0
            })
    
    elif profile.role == 'teacher':
        try:
            teacher = profile.teacher
            sections = Section.objects.filter(teacher=teacher)
            context['sections_count'] = sections.count()
            
            # Count total students across all sections
            total_students = Enrollment.objects.filter(
                section__in=sections, 
                status='enrolled'
            ).count()
            context['students_count'] = total_students
            
        except:
            context.update({
                'sections_count': 0,
                'students_count': 0
            })
    
    return render(request, 'accounts/profile.html', context)

# Admin Views
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        profile = get_object_or_404(Profile, user=request.user)
        if profile.role != UserRole.ADMIN:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def manage_students_view(request):
    students = Student.objects.filter(is_active=True).select_related('profile__user')
    return render(request, 'accounts/manage_students.html', {'students': students})

@admin_required
def manage_teachers_view(request):
    teachers = Teacher.objects.filter(is_active=True).select_related('profile__user')
    return render(request, 'accounts/manage_teachers.html', {'teachers': teachers})

@admin_required
def add_student_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create User
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        password=form.cleaned_data['password1']
                    )
                    
                    # Create Profile
                    profile = Profile.objects.create(
                        user=user,
                        role=UserRole.STUDENT,
                        phone_number=form.cleaned_data.get('phone_number', ''),
                        address=form.cleaned_data.get('address', ''),
                        date_of_birth=form.cleaned_data.get('date_of_birth'),
                        profile_picture=form.cleaned_data.get('profile_picture')
                    )
                    
                    # Create Student
                    Student.objects.create(
                        profile=profile,
                        student_id=form.cleaned_data['student_id'],
                        registration_number=form.cleaned_data['registration_number'],
                        admission_date=form.cleaned_data['admission_date']
                    )
                    
                    messages.success(request, f'Student {user.username} created successfully!')
                    return redirect('accounts:manage_students')
            except Exception as e:
                messages.error(request, f'Error creating student: {str(e)}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/add_student.html', {'form': form})

@admin_required
def add_teacher_view(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create User
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        password=form.cleaned_data['password1']
                    )
                    
                    # Create Profile
                    profile = Profile.objects.create(
                        user=user,
                        role=UserRole.TEACHER,
                        phone_number=form.cleaned_data.get('phone_number', ''),
                        address=form.cleaned_data.get('address', ''),
                        date_of_birth=form.cleaned_data.get('date_of_birth'),
                        profile_picture=form.cleaned_data.get('profile_picture')
                    )
                    
                    # Create Teacher
                    Teacher.objects.create(
                        profile=profile,
                        employee_id=form.cleaned_data['employee_id'],
                        department=form.cleaned_data['department'],
                        qualification=form.cleaned_data['qualification'],
                        experience_years=form.cleaned_data.get('experience_years', 0),
                        join_date=form.cleaned_data['join_date']
                    )
                    
                    messages.success(request, f'Teacher {user.username} created successfully!')
                    return redirect('accounts:manage_teachers')
            except Exception as e:
                messages.error(request, f'Error creating teacher: {str(e)}')
    else:
        form = TeacherRegistrationForm()
    
    return render(request, 'accounts/add_teacher.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user_type = form.cleaned_data['user_type']
            
            # Generate a reset token
            reset_token = str(uuid.uuid4())
            
            # Store the reset token in session (in production, use database or Redis)
            request.session['reset_token'] = reset_token
            request.session['reset_user_id'] = user.id
            request.session['reset_user_type'] = user_type
            
            # In production, you would send an email here
            # For demo purposes, we'll just redirect to reset page
            messages.success(
                request, 
                f'Password reset link has been sent to your email. For demo purposes, you can proceed to reset your password.'
            )
            
            return redirect('accounts:reset_password', token=reset_token)
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'accounts/forgot_password.html', {'form': form})

def reset_password_view(request, token):
    # Verify token
    if request.session.get('reset_token') != token:
        messages.error(request, 'Invalid or expired reset token.')
        return redirect('accounts:login')
    
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Invalid reset session.')
        return redirect('accounts:login')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user.')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            
            # Clear session data
            request.session.pop('reset_token', None)
            request.session.pop('reset_user_id', None)
            request.session.pop('reset_user_type', None)
            
            messages.success(request, 'Your password has been successfully reset. You can now login with your new password.')
            return redirect('accounts:login')
    else:
        form = ResetPasswordForm()
    
    context = {
        'form': form,
        'user': user,
        'token': token
    }
    
    return render(request, 'accounts/reset_password.html', context)

@login_required
def settings_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        # Handle settings update
        user = request.user
        
        # Update basic user info
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Update profile info
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        # Handle password change
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if old_password and new_password and confirm_password:
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password updated successfully!')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Current password is incorrect.')
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('accounts:settings')
    
    context = {
        'profile': profile,
        'user': request.user,
    }
    
    return render(request, 'accounts/settings.html', context)

@login_required
def toggle_pin_view(request):
    """Handle pin/unpin functionality via AJAX"""
    if request.method == 'POST':
        try:
            import json
            
            data = json.loads(request.body)
            item_id = data.get('item_id')
            item_type = data.get('item_type')
            action = data.get('action')
            
            # Here you could save the pinned items to a user preference model
            # For now, we'll just return success since we're using localStorage
            
            return JsonResponse({
                'success': True,
                'message': f'Item {action}ned successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def edit_basic_information(request):
    """Edit basic personal information"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = BasicInformationForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            # Update user fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            
            # Update profile fields
            form.save()
            messages.success(request, 'Basic information updated successfully!')
            return redirect('accounts:profile')
    else:
        form = BasicInformationForm(instance=profile, user=request.user)
    
    return render(request, 'accounts/edit_basic_info.html', {'form': form})

@login_required
def edit_name_pronunciation(request):
    """Edit name pronunciation and pronouns"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = NamePronunciationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Name pronunciation and pronouns updated successfully!')
            return redirect('accounts:profile')
    else:
        form = NamePronunciationForm(instance=profile)
    
    return render(request, 'accounts/edit_name_pronunciation.html', {'form': form})

@login_required
def edit_contact_information(request):
    """Edit contact information"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ContactInformationForm(request.POST, instance=profile)
        if form.is_valid():
            # Update email in User model
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            # Update profile fields
            form.save()
            messages.success(request, 'Contact information updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ContactInformationForm(instance=profile)
        form.fields['email'].initial = request.user.email
    
    return render(request, 'accounts/edit_contact_info.html', {'form': form})

@login_required
def edit_student_information(request):
    """Edit student-specific information"""
    if request.user.profile.role != 'student':
        messages.error(request, 'Access denied. Student account required.')
        return redirect('accounts:profile')
    
    try:
        student = request.user.profile.student
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = StudentInformationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student information updated successfully!')
            return redirect('accounts:profile')
    else:
        form = StudentInformationForm(instance=student)
    
    return render(request, 'accounts/edit_student_info.html', {'form': form})

@login_required
def edit_staff_information(request):
    """Edit staff-specific information"""
    if request.user.profile.role != 'teacher':
        messages.error(request, 'Access denied. Staff account required.')
        return redirect('accounts:profile')
    
    try:
        teacher = request.user.profile.teacher
    except Teacher.DoesNotExist:
        messages.error(request, 'Staff profile not found.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = StaffInformationForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff information updated successfully!')
            return redirect('accounts:profile')
    else:
        form = StaffInformationForm(instance=teacher)
    
    return render(request, 'accounts/edit_staff_info.html', {'form': form})

@login_required
def change_profile_picture(request):
    """Change profile picture"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfilePictureForm(instance=profile)
    
    return render(request, 'accounts/change_picture.html', {'form': form})

@login_required
def delete_profile_picture(request):
    """Delete profile picture"""
    if request.method == 'POST':
        profile = request.user.profile
        if profile.profile_picture:
            profile.profile_picture.delete()
            profile.save()
            messages.success(request, 'Profile picture deleted successfully!')
        else:
            messages.info(request, 'No profile picture to delete.')
        return redirect('accounts:profile')
    return redirect('accounts:profile')

@login_required
def update_status(request):
    """Update user status message"""
    if request.method == 'POST':
        status_message = request.POST.get('status_message', '').strip()
        
        # You can save this to a separate UserStatus model or Profile model
        # For now, we'll use the bio field
        profile = request.user.profile
        profile.bio = status_message
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Status updated successfully!'
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
