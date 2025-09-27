from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile, Student, Teacher, UserRole
from .forms import LoginForm, StudentRegistrationForm, TeacherRegistrationForm, ProfileUpdateForm, ForgotPasswordForm, ResetPasswordForm
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
    profile = get_object_or_404(Profile, user=request.user)
    
    context = {
        'profile': profile,
    }
    
    if profile.role == UserRole.ADMIN:
        # Admin dashboard data
        context.update({
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_teachers': Teacher.objects.filter(is_active=True).count(),
            'total_courses': Section.objects.count(),
        })
        return render(request, 'accounts/admin_dashboard.html', context)
    
    elif profile.role == UserRole.TEACHER:
        # Teacher dashboard data
        teacher = get_object_or_404(Teacher, profile=profile)
        sections = Section.objects.filter(teacher=teacher)
        context.update({
            'teacher': teacher,
            'sections': sections,
            'total_sections': sections.count(),
        })
        return render(request, 'accounts/teacher_dashboard.html', context)
    
    elif profile.role == UserRole.STUDENT:
        # Student dashboard data
        student = get_object_or_404(Student, profile=profile)
        enrollments = Enrollment.objects.filter(student=student, status='enrolled')
        recent_grades = FinalGrade.objects.filter(student=student).order_by('-date_recorded')[:5]
        
        context.update({
            'student': student,
            'enrollments': enrollments,
            'recent_grades': recent_grades,
            'total_courses': enrollments.count(),
        })
        return render(request, 'accounts/student_dashboard.html', context)
    
    return render(request, 'accounts/dashboard.html', context)

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
