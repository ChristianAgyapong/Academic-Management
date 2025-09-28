from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, Avg
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import date, timedelta
import json
from accounts.models import Teacher, Student
from courses.models import Section, Enrollment
from .models import AttendanceSession, Attendance, AttendanceSummary

@login_required
def student_attendance_view(request):
    """
    View student's own attendance across all enrolled sections.
    """
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Access denied. Student account required.')
        return redirect('accounts:dashboard')
    
    student = request.user.student_profile
    
    # Get all attendance summaries for the student
    attendance_summaries = AttendanceSummary.objects.filter(
        student=student
    ).select_related('section__course', 'section__teacher__profile__user')
    
    # Calculate overall statistics
    total_courses = attendance_summaries.count()
    overall_avg = attendance_summaries.aggregate(
        avg=Avg('attendance_percentage')
    )['avg'] or 0
    
    # Count courses with good/poor attendance
    good_attendance = attendance_summaries.filter(attendance_percentage__gte=85).count()
    poor_attendance = attendance_summaries.filter(attendance_percentage__lt=75).count()
    
    # Get recent attendance records
    recent_attendance = Attendance.objects.filter(
        student=student
    ).select_related('session__section__course').order_by('-session__date')[:10]
    
    context = {
        'student': student,
        'attendance_summaries': attendance_summaries,
        'total_courses': total_courses,
        'overall_avg': round(overall_avg, 1),
        'good_attendance': good_attendance,
        'poor_attendance': poor_attendance,
        'recent_attendance': recent_attendance,
    }
    
    return render(request, 'attendance/student_attendance.html', context)

@login_required
def section_attendance_view(request, section_id):
    """
    View attendance records for a specific section.
    """
    try:
        teacher = request.user.profile.teacher
    except:
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('accounts:dashboard')
    
    section = get_object_or_404(Section, id=section_id, teacher=teacher)
    
    # Get all sessions for this section
    sessions = AttendanceSession.objects.filter(section=section).order_by('-date')
    
    # Add attendance counts for each session
    sessions_with_counts = []
    for session in sessions:
        attendance_records = Attendance.objects.filter(session=session)
        session.present_count = attendance_records.filter(status='present').count()
        session.absent_count = attendance_records.filter(status='absent').count()
        session.late_count = attendance_records.filter(status='late').count()
        session.excused_count = attendance_records.filter(status='excused').count()
        sessions_with_counts.append(session)
    
    # Get attendance summaries for all students in this section
    attendance_summaries = AttendanceSummary.objects.filter(
        section=section
    ).select_related('student__profile__user').order_by('student__profile__user__last_name')
    
    # Get recent attendance sessions
    recent_sessions = sessions_with_counts[:10]
    
    # Calculate section statistics
    total_students = Enrollment.objects.filter(section=section, status='enrolled').count()
    total_sessions = sessions.count()
    
    avg_attendance = attendance_summaries.aggregate(
        avg=Avg('attendance_percentage')
    )['avg'] or 0
    
    low_attendance_count = attendance_summaries.filter(
        attendance_percentage__lt=75.0
    ).count()
    
    # Pagination for sessions
    paginator = Paginator(sessions_with_counts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'section': section,
        'sessions': page_obj,
        'attendance_summaries': attendance_summaries,
        'recent_sessions': recent_sessions,
        'total_students': total_students,
        'total_sessions': total_sessions,
        'avg_attendance': round(avg_attendance, 1),
        'low_attendance_count': low_attendance_count,
    }
    
    return render(request, 'attendance/section_attendance.html', context)

@login_required
def teacher_attendance_sections_view(request):
    """
    Display teacher's sections for attendance management with real data.
    """
    try:
        teacher = request.user.profile.teacher
    except:
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('accounts:dashboard')
    
    sections = Section.objects.filter(teacher=teacher).select_related('course', 'semester')
    
    # Calculate statistics
    total_sections = sections.count()
    total_students = Enrollment.objects.filter(
        section__in=sections, 
        status='enrolled'
    ).count()
    
    # Calculate average attendance across all teacher's sections
    attendance_summaries = AttendanceSummary.objects.filter(
        section__in=sections
    )
    average_attendance = attendance_summaries.aggregate(
        avg_attendance=Avg('attendance_percentage')
    )['avg_attendance'] or 0
    
    # Count low attendance alerts (students with < 75% attendance)
    low_attendance_alerts = attendance_summaries.filter(
        attendance_percentage__lt=75.0
    ).count()
    
    # Get recent attendance sessions
    recent_sessions = AttendanceSession.objects.filter(
        section__in=sections
    ).order_by('-date')[:5]
    
    # Prepare section data with statistics
    sections_data = []
    for section in sections:
        enrolled_students = Enrollment.objects.filter(
            section=section, 
            status='enrolled'
        ).count()
        
        total_sessions = AttendanceSession.objects.filter(section=section).count()
        
        section_avg_attendance = AttendanceSummary.objects.filter(
            section=section
        ).aggregate(avg=Avg('attendance_percentage'))['avg'] or 0
        
        alerts = AttendanceSummary.objects.filter(
            section=section,
            attendance_percentage__lt=75.0
        ).count()
        
        sections_data.append({
            'section': section,
            'enrolled_students': enrolled_students,
            'total_sessions': total_sessions,
            'average_attendance': round(section_avg_attendance, 1),
            'low_attendance_alerts': alerts,
        })
    
    context = {
        'page_title': 'Attendance Management',
        'total_sections': total_sections,
        'total_students': total_students,
        'average_attendance': round(average_attendance, 1),
        'low_attendance_alerts': low_attendance_alerts,
        'sections_data': sections_data,
        'recent_sessions': recent_sessions,
        'teacher': teacher,
    }
    return render(request, 'attendance/teacher_attendance_sections.html', context)

@login_required
def mark_attendance_view(request, section_id):
    """
    Mark attendance for a specific section.
    """
    try:
        teacher = request.user.profile.teacher
    except:
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('accounts:dashboard')
    
    section = get_object_or_404(Section, id=section_id, teacher=teacher)
    
    if request.method == 'POST':
        # Create or get attendance session
        session_date = request.POST.get('session_date', date.today())
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        topic_covered = request.POST.get('topic_covered', '')
        notes = request.POST.get('session_notes', '')
        
        # Handle empty time fields
        start_time = start_time if start_time and start_time.strip() else None
        end_time = end_time if end_time and end_time.strip() else None
        
        session, created = AttendanceSession.objects.get_or_create(
            section=section,
            date=session_date,
            start_time=start_time,
            defaults={
                'end_time': end_time,
                'topic_covered': topic_covered,
                'notes': notes
            }
        )
        
        if not created:
            session.end_time = end_time
            session.topic_covered = topic_covered
            session.notes = notes
            session.save()
        
        # Process attendance data
        students = Enrollment.objects.filter(section=section, status='enrolled')
        
        for enrollment in students:
            student_id = str(enrollment.student.id)
            status = request.POST.get(f'attendance_{student_id}', 'absent')
            arrival_time = request.POST.get(f'arrival_time_{student_id}')
            student_notes = request.POST.get(f'notes_{student_id}', '')
            
            # Handle empty arrival_time field
            arrival_time = arrival_time if arrival_time and arrival_time.strip() else None
            
            # Create or update attendance record
            attendance, created = Attendance.objects.update_or_create(
                student=enrollment.student,
                session=session,
                defaults={
                    'status': status,
                    'arrival_time': arrival_time,
                    'notes': student_notes,
                    'marked_by': request.user.get_full_name() or request.user.username
                }
            )
            
            # Update or create attendance summary
            summary, created = AttendanceSummary.objects.get_or_create(
                student=enrollment.student,
                section=section
            )
            summary.update_summary()
        
        messages.success(request, f'Attendance marked successfully for {session.date}')
        return redirect('attendance:section_attendance', section_id=section.id)
    
    # GET request - show attendance marking form
    students = Enrollment.objects.filter(section=section, status='enrolled').select_related('student__profile__user')
    today_session = AttendanceSession.objects.filter(section=section, date=date.today()).first()
    
    # Get existing attendance if session exists
    existing_attendance = {}
    if today_session:
        attendance_records = Attendance.objects.filter(session=today_session)
        existing_attendance = {record.student.id: record for record in attendance_records}
    
    context = {
        'section': section,
        'students': students,
        'today_session': today_session,
        'existing_attendance': existing_attendance,
        'current_date': date.today(),
        'current_time': timezone.now().time().strftime('%H:%M'),
    }
    
    return render(request, 'attendance/mark_attendance.html', context)

@login_required
def attendance_history_view(request, section_id):
    """
    View detailed attendance history for a section.
    """
    try:
        teacher = request.user.profile.teacher
    except:
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('accounts:dashboard')
    
    section = get_object_or_404(Section, id=section_id, teacher=teacher)
    
    # Get all sessions and attendance records
    sessions = AttendanceSession.objects.filter(section=section).order_by('-date')
    
    # Prepare attendance matrix (students x sessions)
    students = Enrollment.objects.filter(
        section=section, 
        status='enrolled'
    ).select_related('student__profile__user')
    
    attendance_matrix = {}
    for student in students:
        student_attendance = {}
        for session in sessions:
            try:
                attendance = Attendance.objects.get(student=student.student, session=session)
                student_attendance[session.id] = attendance
            except Attendance.DoesNotExist:
                student_attendance[session.id] = None
        attendance_matrix[student.student.id] = student_attendance
    
    context = {
        'section': section,
        'sessions': sessions,
        'students': students,
        'attendance_matrix': attendance_matrix,
    }
    
    return render(request, 'attendance/attendance_history.html', context)

@login_required
def attendance_reports_view(request):
    """
    Generate attendance reports for teachers.
    """
    try:
        teacher = request.user.profile.teacher
    except:
        messages.error(request, 'Access denied. Teacher account required.')
        return redirect('accounts:dashboard')
    sections = Section.objects.filter(teacher=teacher)
    
    # Filter by section if specified
    selected_section_id = request.GET.get('section')
    selected_section = None
    if selected_section_id:
        selected_section = get_object_or_404(Section, id=selected_section_id, teacher=teacher)
        sections = sections.filter(id=selected_section_id)
    
    # Generate report data
    report_data = []
    for section in sections:
        summaries = AttendanceSummary.objects.filter(section=section)
        section_data = {
            'section': section,
            'total_students': summaries.count(),
            'avg_attendance': summaries.aggregate(avg=Avg('attendance_percentage'))['avg'] or 0,
            'excellent_count': summaries.filter(attendance_percentage__gte=90).count(),
            'good_count': summaries.filter(attendance_percentage__gte=75, attendance_percentage__lt=90).count(),
            'poor_count': summaries.filter(attendance_percentage__lt=75).count(),
        }
        report_data.append(section_data)
    
    context = {
        'teacher_sections': Section.objects.filter(teacher=teacher),
        'selected_section': selected_section,
        'report_data': report_data,
    }
    
    return render(request, 'attendance/attendance_reports.html', context)

@login_required
def export_attendance_csv(request, section_id):
    """
    Export attendance data as CSV file.
    """
    try:
        teacher = request.user.profile.teacher
    except:
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    section = get_object_or_404(Section, id=section_id, teacher=teacher)
    
    import csv
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{section.course.code}_{section.section_number}.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    sessions = AttendanceSession.objects.filter(section=section).order_by('date')
    header = ['Student ID', 'Student Name', 'Total Sessions', 'Present', 'Absent', 'Late', 'Excused', 'Attendance %']
    header.extend([f"{session.date}" for session in sessions])
    writer.writerow(header)
    
    # Write student data
    students = Enrollment.objects.filter(section=section, status='enrolled')
    for enrollment in students:
        student = enrollment.student
        summary = AttendanceSummary.objects.filter(student=student, section=section).first()
        
        if summary:
            row = [
                student.profile.user.username,
                student.profile.user.get_full_name(),
                summary.total_sessions,
                summary.present_count,
                summary.absent_count,
                summary.late_count,
                summary.excused_count,
                f"{summary.attendance_percentage:.1f}%"
            ]
        else:
            row = [
                student.profile.user.username,
                student.profile.user.get_full_name(),
                0, 0, 0, 0, 0, "0.0%"
            ]
        
        # Add attendance for each session
        for session in sessions:
            try:
                attendance = Attendance.objects.get(student=student, session=session)
                row.append(attendance.get_status_display())
            except Attendance.DoesNotExist:
                row.append('Not Recorded')
        
        writer.writerow(row)
    
    return response
