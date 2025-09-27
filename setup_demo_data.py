#!/usr/bin/env python
"""
SAMS Demo Data Setup Script
Creates comprehensive demo data including admin users, students, teachers, courses, and more.
"""

import os
import sys
import django
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile, Student, Teacher
from courses.models import Course, Section, Enrollment, AcademicYear, Semester
from grades.models import Grade, GradeComponent
from attendance.models import Attendance, AttendanceSession
from datetime import datetime, timedelta, date
import random


def create_admin_users():
    """Create admin and superuser accounts"""
    print("Creating admin users...")
    
    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@sams.com',
            password='admin123',
            first_name='System',
            last_name='Administrator'
        )
        print(f"✓ Created superuser: admin / admin123")
    else:
        admin_user = User.objects.get(username='admin')
        print(f"✓ Superuser already exists: admin")
    
    # Ensure admin has profile
    if not hasattr(admin_user, 'profile'):
        Profile.objects.create(
            user=admin_user,
            role='admin',
            phone_number='+233-20-123-4567',
            address='University Campus, Accra'
        )
        print(f"✓ Created profile for admin user")


def create_demo_teachers():
    """Create demo teacher accounts"""
    print("\nCreating demo teachers...")
    
    teachers_data = [
        {
            'username': 'dr.mensah',
            'email': 'k.mensah@ug.edu.gh',
            'first_name': 'Dr. Kwame',
            'last_name': 'Mensah',
            'employee_id': 'UG001',
            'department': 'Computer Science',
            'phone': '+233-24-111-2233',
            'password': 'teacher123'
        },
        {
            'username': 'prof.asante',
            'email': 'a.asante@ug.edu.gh',
            'first_name': 'Prof. Akosua',
            'last_name': 'Asante',
            'employee_id': 'UG002',
            'department': 'Mathematics',
            'phone': '+233-24-222-3344',
            'password': 'teacher123'
        },
        {
            'username': 'dr.osei',
            'email': 'm.osei@ug.edu.gh',
            'first_name': 'Dr. Michael',
            'last_name': 'Osei',
            'employee_id': 'UG003',
            'department': 'Physics',
            'phone': '+233-24-333-4455',
            'password': 'teacher123'
        },
        {
            'username': 'ms.antwi',
            'email': 'g.antwi@ug.edu.gh',
            'first_name': 'Ms. Grace',
            'last_name': 'Antwi',
            'employee_id': 'UG004',
            'department': 'English Literature',
            'phone': '+233-24-444-5566',
            'password': 'teacher123'
        }
    ]
    
    for teacher_data in teachers_data:
        if not User.objects.filter(username=teacher_data['username']).exists():
            # Create user
            user = User.objects.create_user(
                username=teacher_data['username'],
                email=teacher_data['email'],
                password=teacher_data['password'],
                first_name=teacher_data['first_name'],
                last_name=teacher_data['last_name']
            )
            
            # Create profile
            profile = Profile.objects.create(
                user=user,
                role='teacher',
                phone_number=teacher_data['phone'],
                address='University Campus, Accra'
            )
            
            # Create teacher record
            Teacher.objects.create(
                profile=profile,
                employee_id=teacher_data['employee_id'],
                department=teacher_data['department'],
                qualification='PhD in ' + teacher_data['department'],
                experience_years=random.randint(5, 20),
                join_date=date.today() - timedelta(days=random.randint(365, 3650))
            )
            
            print(f"✓ Created teacher: {teacher_data['username']} / {teacher_data['password']}")
        else:
            print(f"✓ Teacher already exists: {teacher_data['username']}")


def create_demo_students():
    """Create demo student accounts"""
    print("\nCreating demo students...")
    
    students_data = [
        {
            'username': 'student001',
            'email': 'kwame.nkrumah@st.ug.edu.gh',
            'first_name': 'Kwame',
            'last_name': 'Nkrumah',
            'student_id': '10957023',
            'year_of_study': 3,
            'program': 'Computer Science',
            'phone': '+233-20-111-2233',
            'password': 'student123'
        },
        {
            'username': 'student002',
            'email': 'ama.aidoo@st.ug.edu.gh',
            'first_name': 'Ama',
            'last_name': 'Aidoo',
            'student_id': '10957024',
            'year_of_study': 2,
            'program': 'Mathematics',
            'phone': '+233-20-222-3344',
            'password': 'student123'
        },
        {
            'username': 'student003',
            'email': 'kofi.annan@st.ug.edu.gh',
            'first_name': 'Kofi',
            'last_name': 'Annan',
            'student_id': '10957025',
            'year_of_study': 4,
            'program': 'International Relations',
            'phone': '+233-20-333-4455',
            'password': 'student123'
        },
        {
            'username': 'student004',
            'email': 'akosua.frema@st.ug.edu.gh',
            'first_name': 'Akosua',
            'last_name': 'Frema',
            'student_id': '10957026',
            'year_of_study': 1,
            'program': 'Physics',
            'phone': '+233-20-444-5566',
            'password': 'student123'
        },
        {
            'username': 'student005',
            'email': 'yaw.asante@st.ug.edu.gh',
            'first_name': 'Yaw',
            'last_name': 'Asante',
            'student_id': '10957027',
            'year_of_study': 3,
            'program': 'Business Administration',
            'phone': '+233-20-555-6677',
            'password': 'student123'
        },
        {
            'username': 'student006',
            'email': 'efua.sutherland@st.ug.edu.gh',
            'first_name': 'Efua',
            'last_name': 'Sutherland',
            'student_id': '10957028',
            'year_of_study': 2,
            'program': 'English Literature',
            'phone': '+233-20-666-7788',
            'password': 'student123'
        }
    ]
    
    for student_data in students_data:
        if not User.objects.filter(username=student_data['username']).exists():
            # Create user
            user = User.objects.create_user(
                username=student_data['username'],
                email=student_data['email'],
                password=student_data['password'],
                first_name=student_data['first_name'],
                last_name=student_data['last_name']
            )
            
            # Create profile
            profile = Profile.objects.create(
                user=user,
                role='student',
                phone_number=student_data['phone'],
                address='Student Hostel, University of Ghana'
            )
            
            # Create student record
            Student.objects.create(
                profile=profile,
                student_id=student_data['student_id'],
                registration_number=f"REG{student_data['student_id']}",
                admission_date=date.today() - timedelta(days=random.randint(365, 1460))
            )
            
            print(f"✓ Created student: {student_data['username']} / {student_data['password']}")
        else:
            print(f"✓ Student already exists: {student_data['username']}")


def create_academic_structure():
    """Create academic year and semester"""
    print("\nCreating academic structure...")
    
    # Create current academic year
    current_year = datetime.now().year
    academic_year, created = AcademicYear.objects.get_or_create(
        name=f"{current_year}-{current_year + 1}",
        defaults={
            'start_date': date(current_year, 8, 1),
            'end_date': date(current_year + 1, 7, 31),
            'is_current': True
        }
    )
    if created:
        print(f"✓ Created academic year: {academic_year.name}")
    
    # Create current semester
    semester, created = Semester.objects.get_or_create(
        name=f"Fall {current_year}",
        academic_year=academic_year,
        defaults={
            'start_date': date(current_year, 8, 1),
            'end_date': date(current_year, 12, 31),
            'is_current': True
        }
    )
    if created:
        print(f"✓ Created semester: {semester.name}")
    
    return academic_year, semester


def create_demo_courses():
    """Create demo courses and sections"""
    print("\nCreating demo courses...")
    
    # Get current semester
    try:
        semester = Semester.objects.get(is_current=True)
    except Semester.DoesNotExist:
        print("✗ No current semester found. Creating academic structure first...")
        _, semester = create_academic_structure()
    
    courses_data = [
        {
            'code': 'CS101',
            'name': 'Introduction to Computer Science',
            'description': 'Fundamental concepts of computer science and programming.',
            'credits': 3,
            'department': 'Computer Science',
            'teacher_employee_id': 'UG001'
        },
        {
            'code': 'MATH201',
            'name': 'Calculus II',
            'description': 'Advanced calculus including integration and series.',
            'credits': 4,
            'department': 'Mathematics',
            'teacher_employee_id': 'UG002'
        },
        {
            'code': 'PHYS101',
            'name': 'General Physics I',
            'description': 'Mechanics, waves, and thermodynamics.',
            'credits': 4,
            'department': 'Physics',
            'teacher_employee_id': 'UG003'
        },
        {
            'code': 'ENG102',
            'name': 'Academic Writing',
            'description': 'Advanced academic writing and research skills.',
            'credits': 2,
            'department': 'English',
            'teacher_employee_id': 'UG004'
        },
        {
            'code': 'CS201',
            'name': 'Data Structures and Algorithms',
            'description': 'Advanced programming concepts and algorithm design.',
            'credits': 3,
            'department': 'Computer Science',
            'teacher_employee_id': 'UG001'
        }
    ]
    
    for course_data in courses_data:
        if not Course.objects.filter(code=course_data['code']).exists():
            course = Course.objects.create(
                code=course_data['code'],
                name=course_data['name'],
                description=course_data['description'],
                credits=course_data['credits'],
                department=course_data['department']
            )
            print(f"✓ Created course: {course_data['code']} - {course_data['name']}")
            
            # Create section for this course
            try:
                teacher = Teacher.objects.get(employee_id=course_data['teacher_employee_id'])
                section = Section.objects.create(
                    course=course,
                    semester=semester,
                    teacher=teacher,
                    section_number='001',
                    max_capacity=30,
                    schedule='MWF 10:00-11:00 AM',
                    classroom=f'Room {random.randint(100, 299)}'
                )
                print(f"✓ Created section for {course_data['code']}")
            except Teacher.DoesNotExist:
                print(f"✗ Teacher {course_data['teacher_employee_id']} not found for course {course_data['code']}")
        else:
            print(f"✓ Course already exists: {course_data['code']}")


def create_demo_enrollments():
    """Create demo enrollments"""
    print("\nCreating demo enrollments...")
    
    # Enroll students in sections
    enrollments = [
        ('10957023', 'CS101'),
        ('10957023', 'MATH201'),
        ('10957023', 'CS201'),
        ('10957024', 'MATH201'),
        ('10957024', 'PHYS101'),
        ('10957025', 'ENG102'),
        ('10957025', 'CS101'),
        ('10957026', 'PHYS101'),
        ('10957026', 'MATH201'),
        ('10957027', 'CS101'),
        ('10957027', 'ENG102'),
        ('10957028', 'ENG102'),
        ('10957028', 'CS101')
    ]
    
    for student_id, course_code in enrollments:
        try:
            student = Student.objects.get(student_id=student_id)
            course = Course.objects.get(code=course_code)
            section = Section.objects.filter(course=course).first()
            
            if section and not Enrollment.objects.filter(student=student, section=section).exists():
                enrollment = Enrollment.objects.create(
                    student=student,
                    section=section,
                    status='enrolled'
                )
                print(f"✓ Enrolled {student.profile.user.get_full_name()} in {course_code}")
            else:
                print(f"✓ Enrollment already exists: {student_id} in {course_code}")
        except (Student.DoesNotExist, Course.DoesNotExist) as e:
            print(f"✗ Error enrolling {student_id} in {course_code}: {e}")


def create_demo_grades():
    """Create demo grades and grade components"""
    print("\nCreating demo grades...")
    
    sections = Section.objects.all()
    grade_values = [85, 92, 78, 88, 94, 76, 82, 90, 86, 79, 91, 84]
    
    for section in sections:
        # Create grade components for each section
        components_data = [
            {'name': 'Midterm Exam', 'weight': 30, 'max_points': 100},
            {'name': 'Final Exam', 'weight': 40, 'max_points': 100},
            {'name': 'Assignments', 'weight': 20, 'max_points': 100},
            {'name': 'Participation', 'weight': 10, 'max_points': 100}
        ]
        
        for comp_data in components_data:
            component, created = GradeComponent.objects.get_or_create(
                section=section,
                name=comp_data['name'],
                defaults={
                    'weight_percentage': comp_data['weight'],
                    'max_points': comp_data['max_points']
                }
            )
            if created:
                print(f"✓ Created grade component: {comp_data['name']} for {section.course.code}")
        
        # Create grades for enrolled students
        enrollments = Enrollment.objects.filter(section=section)
        for enrollment in enrollments:
            components = GradeComponent.objects.filter(section=section)
            for component in components:
                if not Grade.objects.filter(student=enrollment.student, component=component).exists():
                    points_earned = random.choice(grade_values)
                    Grade.objects.create(
                        student=enrollment.student,
                        section=section,
                        component=component,
                        points_earned=points_earned,
                        comments=f"Good work on {component.name}"
                    )
            
            print(f"✓ Created grades for {enrollment.student.profile.user.get_full_name()} in {section.course.code}")


def create_demo_attendance():
    """Create demo attendance records"""
    print("\nCreating demo attendance records...")
    
    sections = Section.objects.all()
    
    for section in sections:
        enrollments = Enrollment.objects.filter(section=section)
        
        # Create attendance sessions for the past month
        for i in range(15):  # 15 class sessions
            session_date = datetime.now().date() - timedelta(days=i*2)  # Every other day
            
            session, created = AttendanceSession.objects.get_or_create(
                section=section,
                date=session_date,
                defaults={
                    'start_time': datetime.strptime('10:00', '%H:%M').time(),
                    'end_time': datetime.strptime('11:00', '%H:%M').time(),
                    'topic_covered': f'Class topic for {session_date}',
                    'notes': 'Regular class session'
                }
            )
            
            if created:
                # Create attendance records for each enrolled student
                for enrollment in enrollments:
                    # 85% attendance rate
                    status = 'present' if random.random() > 0.15 else 'absent'
                    Attendance.objects.create(
                        student=enrollment.student,
                        session=session,
                        status=status,
                        marked_by=section.teacher.profile.user.get_full_name()
                    )
        
        print(f"✓ Created attendance records for {section.course.code}")


def print_demo_credentials():
    """Print all demo login credentials"""
    print("\n" + "="*80)
    print("🎓 SAMS DEMO SYSTEM - LOGIN CREDENTIALS")
    print("="*80)
    
    print("\n👑 ADMIN ACCESS:")
    print("-" * 40)
    print("🔗 Admin Panel: http://127.0.0.1:8000/admin/")
    print("👤 Username: admin")
    print("🔑 Password: admin123")
    print("📧 Email: admin@sams.com")
    
    print("\n📚 TEACHER ACCOUNTS:")
    print("-" * 40)
    teachers = Teacher.objects.all()
    for teacher in teachers:
        print(f"👤 Username: {teacher.profile.user.username}")
        print(f"🔑 Password: teacher123")
        print(f"🆔 Employee ID: {teacher.employee_id}")
        print(f"📧 Email: {teacher.profile.user.email}")
        print(f"🏢 Department: {teacher.department}")
        print("")
    
    print("🎓 STUDENT ACCOUNTS:")
    print("-" * 40)
    students = Student.objects.all()
    for student in students:
        print(f"👤 Username: {student.profile.user.username}")
        print(f"🔑 Password: student123")
        print(f"🆔 Student ID: {student.student_id}")
        print(f"📧 Email: {student.profile.user.email}")
        print(f"🏫 Registration: {student.registration_number}")
        print("")
    
    print("🔗 MAIN APPLICATION:")
    print("-" * 40)
    print("🏠 Login Page: http://127.0.0.1:8000/login/")
    print("🔄 Forgot Password: http://127.0.0.1:8000/forgot-password/")
    
    print("\n📊 SYSTEM STATISTICS:")
    print("-" * 40)
    print(f"👥 Total Users: {User.objects.count()}")
    print(f"🎓 Students: {Student.objects.count()}")
    print(f"👨‍🏫 Teachers: {Teacher.objects.count()}")
    print(f"📚 Courses: {Course.objects.count()}")
    print(f"✏️ Enrollments: {Enrollment.objects.count()}")
    print(f"📈 Grades: {Grade.objects.count()}")
    print(f"✅ Attendance Records: {Attendance.objects.count()}")
    
    print("\n" + "="*80)


def main():
    """Main setup function"""
    print("🚀 Setting up SAMS Demo Data...")
    print("=" * 50)
    
    try:
        with transaction.atomic():
            create_admin_users()
            create_demo_teachers()
            create_demo_students()
            create_academic_structure()
            create_demo_courses()
            create_demo_enrollments()
            create_demo_grades()
            create_demo_attendance()
        
        print("\n✅ Demo data setup completed successfully!")
        print_demo_credentials()
        
    except Exception as e:
        print(f"\n❌ Error setting up demo data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()