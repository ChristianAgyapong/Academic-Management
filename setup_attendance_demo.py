#!/usr/bin/env python
"""
Setup script to create sample attendance data for demonstration.
This script creates sample courses, sections, enrollments, and attendance records.
"""
import os
import sys
import django
from datetime import date, time, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile, Student, Teacher
from courses.models import Course, Section, Semester, AcademicYear, Enrollment
from attendance.models import AttendanceSession, Attendance, AttendanceSummary

def setup_attendance_demo_data():
    """Create comprehensive demo data for attendance system testing."""
    
    print("🎯 Setting up Chrix Tech Academic Attendance Demo Data...")
    
    # Create academic year and semester if they don't exist
    academic_year, created = AcademicYear.objects.get_or_create(
        name="2024-2025",
        defaults={
            'start_date': date(2024, 9, 1),
            'end_date': date(2025, 5, 31),
            'is_current': True
        }
    )
    if created:
        print(f"✅ Created academic year: {academic_year.name}")
    
    semester, created = Semester.objects.get_or_create(
        name="Fall 2024",
        academic_year=academic_year,
        defaults={
            'start_date': date(2024, 9, 1),
            'end_date': date(2024, 12, 15),
            'is_current': True
        }
    )
    if created:
        print(f"✅ Created semester: {semester.name}")
    
    # Create sample courses
    courses_data = [
        {
            'code': 'CS101',
            'name': 'Introduction to Computer Science',
            'credits': 3,
            'department': 'Computer Science',
            'description': 'Fundamental concepts of computer science and programming.'
        },
        {
            'code': 'MATH201',
            'name': 'Calculus II',
            'credits': 4,
            'department': 'Mathematics',
            'description': 'Advanced calculus concepts and applications.'
        },
        {
            'code': 'ENG102',
            'name': 'Academic Writing',
            'credits': 3,
            'department': 'English',
            'description': 'Advanced writing skills for academic contexts.'
        }
    ]
    
    courses = {}
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            code=course_data['code'],
            defaults=course_data
        )
        courses[course_data['code']] = course
        if created:
            print(f"✅ Created course: {course.code} - {course.name}")
    
    # Get or create teachers
    teacher_usernames = ['ms.antwi', 'prof.johnson', 'dr.smith']
    teachers = {}
    
    for username in teacher_usernames:
        try:
            user = User.objects.get(username=username)
            if hasattr(user, 'teacher_profile'):
                teachers[username] = user.teacher_profile
                print(f"✅ Found teacher: {username}")
            else:
                print(f"⚠️  User {username} exists but is not a teacher")
        except User.DoesNotExist:
            print(f"⚠️  Teacher {username} not found - creating sample teacher")
            # Create sample teacher
            user = User.objects.create_user(
                username=username,
                email=f'{username}@cta.com',
                first_name=username.split('.')[1].title(),
                last_name=username.split('.')[0].title(),
                password='teacher123'
            )
            profile = Profile.objects.create(user=user, role='teacher')
            teacher = Teacher.objects.create(
                profile=profile, 
                employee_id=f'T{len(teachers)+1001}',
                department='Faculty',
                qualification='PhD',
                experience_years=5,
                join_date=date(2024, 1, 15)
            )
            teachers[username] = teacher
            print(f"✅ Created teacher: {username}")
    
    # Create sections if we have teachers
    if teachers:
        teacher_list = list(teachers.values())
        sections_data = [
            {
                'course': courses['CS101'],
                'section_number': '001',
                'teacher': teacher_list[0] if len(teacher_list) > 0 else None,
                'schedule': 'MWF 9:00-10:00 AM',
                'classroom': 'Room 201',
                'max_capacity': 30
            },
            {
                'course': courses['MATH201'],
                'section_number': '002',
                'teacher': teacher_list[1] if len(teacher_list) > 1 else teacher_list[0],
                'schedule': 'TTh 11:00-12:30 PM',
                'classroom': 'Room 105',
                'max_capacity': 25
            },
            {
                'course': courses['ENG102'],
                'section_number': '001',
                'teacher': teacher_list[2] if len(teacher_list) > 2 else teacher_list[0],
                'schedule': 'MW 2:00-3:30 PM',
                'classroom': 'Room 304',
                'max_capacity': 20
            }
        ]
        
        sections = []
        for section_data in sections_data:
            if section_data['teacher']:
                section, created = Section.objects.get_or_create(
                    course=section_data['course'],
                    semester=semester,
                    section_number=section_data['section_number'],
                    teacher=section_data['teacher'],
                    defaults={
                        'schedule': section_data['schedule'],
                        'classroom': section_data['classroom'],
                        'max_capacity': section_data['max_capacity']
                    }
                )
                sections.append(section)
                if created:
                    print(f"✅ Created section: {section.course.code}-{section.section_number}")
        
        # Get or create students
        student_usernames = ['student001', 'student002', 'student003', 'john.doe', 'jane.smith']
        students = {}
        
        for username in student_usernames:
            try:
                user = User.objects.get(username=username)
                if hasattr(user, 'student_profile'):
                    students[username] = user.student_profile
                    print(f"✅ Found student: {username}")
                else:
                    print(f"⚠️  User {username} exists but is not a student")
            except User.DoesNotExist:
                print(f"⚠️  Student {username} not found - creating sample student")
                # Create sample student
                names = username.replace('.', ' ').split()
                first_name = names[0].title()
                last_name = names[1].title() if len(names) > 1 else 'Student'
                
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@cta.com',
                    first_name=first_name,
                    last_name=last_name,
                    password='student123'
                )
                profile = Profile.objects.create(user=user, role='student')
                student = Student.objects.create(
                    profile=profile, 
                    student_id=f'S{len(students)+2001}',
                    enrollment_date=date(2024, 9, 1)
                )
                students[username] = student
                print(f"✅ Created student: {username}")
        
        # Create enrollments
        if students and sections:
            student_list = list(students.values())
            
            for section in sections:
                # Enroll 3-5 students per section
                enrolled_count = min(len(student_list), 4)
                for i in range(enrolled_count):
                    student = student_list[i % len(student_list)]
                    enrollment, created = Enrollment.objects.get_or_create(
                        student=student,
                        section=section,
                        defaults={'status': 'enrolled'}
                    )
                    if created:
                        print(f"✅ Enrolled {student.profile.user.username} in {section.course.code}-{section.section_number}")
            
            # Create sample attendance sessions and records
            print("📅 Creating attendance sessions and records...")
            
            for section in sections:
                enrolled_students = Enrollment.objects.filter(section=section, status='enrolled')
                
                # Create attendance sessions for the past 2 weeks
                session_dates = []
                base_date = date.today() - timedelta(days=14)
                
                # Create sessions based on schedule (simplified)
                for i in range(8):  # 8 sessions over 2 weeks
                    session_date = base_date + timedelta(days=i*2)  # Every other day
                    session_dates.append(session_date)
                
                for session_date in session_dates:
                    session, created = AttendanceSession.objects.get_or_create(
                        section=section,
                        date=session_date,
                        start_time=time(9, 0),  # 9:00 AM
                        defaults={
                            'end_time': time(10, 30),  # 10:30 AM
                            'topic_covered': f'Lesson {session_dates.index(session_date) + 1}',
                            'notes': f'Regular class session for {session_date}'
                        }
                    )
                    
                    if created:
                        print(f"  📝 Created session: {section.course.code} on {session_date}")
                        
                        # Create attendance records for each enrolled student
                        for enrollment in enrolled_students:
                            # Simulate realistic attendance patterns
                            import random
                            attendance_probability = random.uniform(0.7, 0.95)  # 70-95% attendance rate
                            
                            if random.random() < attendance_probability:
                                if random.random() < 0.9:  # 90% present when attending
                                    status = 'present'
                                else:  # 10% late when attending
                                    status = 'late'
                            else:
                                if random.random() < 0.3:  # 30% excused when absent
                                    status = 'excused'
                                else:  # 70% absent when not attending
                                    status = 'absent'
                            
                            arrival_time = None
                            if status in ['present', 'late']:
                                if status == 'late':
                                    arrival_time = time(9, 15)  # 15 minutes late
                                else:
                                    arrival_time = time(9, 0)  # On time
                            
                            attendance, created = Attendance.objects.get_or_create(
                                student=enrollment.student,
                                session=session,
                                defaults={
                                    'status': status,
                                    'arrival_time': arrival_time,
                                    'marked_by': section.teacher.profile.user.get_full_name(),
                                    'notes': 'Auto-generated demo data'
                                }
                            )
                            
                            # Update attendance summary
                            summary, created = AttendanceSummary.objects.get_or_create(
                                student=enrollment.student,
                                section=section
                            )
                            summary.update_summary()
                            
                        print(f"    ✅ Created attendance records for {enrolled_students.count()} students")
    
    print("\n🎉 Demo data setup completed successfully!")
    print("\n📊 Summary:")
    print(f"   • Academic Years: {AcademicYear.objects.count()}")
    print(f"   • Semesters: {Semester.objects.count()}")
    print(f"   • Courses: {Course.objects.count()}")
    print(f"   • Sections: {Section.objects.count()}")
    print(f"   • Students: {Student.objects.count()}")
    print(f"   • Teachers: {Teacher.objects.count()}")
    print(f"   • Enrollments: {Enrollment.objects.count()}")
    print(f"   • Attendance Sessions: {AttendanceSession.objects.count()}")
    print(f"   • Attendance Records: {Attendance.objects.count()}")
    print(f"   • Attendance Summaries: {AttendanceSummary.objects.count()}")
    
    print("\n🔑 Test Accounts:")
    print("   Teachers:")
    for username in teacher_usernames:
        if User.objects.filter(username=username).exists():
            print(f"     • {username} / password: teacher123")
    
    print("   Students:")
    student_usernames = ['student001', 'student002', 'student003', 'john.doe', 'jane.smith']
    for username in student_usernames:
        if User.objects.filter(username=username).exists():
            print(f"     • {username} / password: student123")
    
    print(f"\n🌐 Access the system at: http://127.0.0.1:8000")
    print("📚 Navigate to Attendance Management to see the demo data in action!")

if __name__ == '__main__':
    setup_attendance_demo_data()