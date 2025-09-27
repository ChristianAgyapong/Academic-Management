from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, Student, Teacher, UserRole
from django.utils import timezone
from datetime import date


class Command(BaseCommand):
    help = 'Create demo users for testing the system'

    def handle(self, *args, **options):
        # Create a demo student
        student_user, created = User.objects.get_or_create(
            username='student001',
            defaults={
                'email': 'student@sams.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        
        if created:
            student_user.set_password('student123')
            student_user.save()
            
            # Create profile
            profile = Profile.objects.create(
                user=student_user,
                role=UserRole.STUDENT,
                phone_number='0555123456',
                address='123 Student Street, Accra',
                date_of_birth=date(2000, 1, 15)
            )
            
            # Create student record
            Student.objects.create(
                profile=profile,
                student_id='STU001',
                registration_number='REG2024001',
                admission_date=date(2024, 9, 1)
            )
            
            self.stdout.write(
                self.style.SUCCESS('Demo student created: username=student001, password=student123')
            )
        else:
            self.stdout.write('Demo student already exists')

        # Create a demo teacher
        teacher_user, created = User.objects.get_or_create(
            username='teacher001',
            defaults={
                'email': 'teacher@sams.com',
                'first_name': 'Jane',
                'last_name': 'Smith'
            }
        )
        
        if created:
            teacher_user.set_password('teacher123')
            teacher_user.save()
            
            # Create profile
            profile = Profile.objects.create(
                user=teacher_user,
                role=UserRole.TEACHER,
                phone_number='0555654321',
                address='456 Teacher Avenue, Accra',
                date_of_birth=date(1985, 5, 20)
            )
            
            # Create teacher record
            Teacher.objects.create(
                profile=profile,
                employee_id='EMP001',
                department='Computer Science',
                qualification='PhD in Computer Science',
                experience_years=8,
                join_date=date(2020, 8, 15)
            )
            
            self.stdout.write(
                self.style.SUCCESS('Demo teacher created: username=teacher001, password=teacher123')
            )
        else:
            self.stdout.write('Demo teacher already exists')

        self.stdout.write(
            self.style.SUCCESS('\n=== Demo Users Created ===')
        )
        self.stdout.write('Student Login:')
        self.stdout.write('  Username: student001')
        self.stdout.write('  Password: student123')
        self.stdout.write('  Student ID: STU001')
        self.stdout.write('')
        self.stdout.write('Teacher Login:')
        self.stdout.write('  Username: teacher001') 
        self.stdout.write('  Password: teacher123')
        self.stdout.write('  Employee ID: EMP001')
        self.stdout.write('')
        self.stdout.write('Admin Login:')
        self.stdout.write('  Username: admin')
        self.stdout.write('  Password: [your admin password]')