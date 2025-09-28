# Student Academic Management System (SAMS)

A comprehensive web-based academic management system built with Django, designed to streamline academic operations for educational institutions.

## 🎯 Features

### 👨‍💼 Administrator Features
- **User Management**: Add, update, and manage students and teachers
- **Course Management**: Create and manage courses, subjects, and timetables
- **Assignment Management**: Assign teachers to courses and sections
- **Report Generation**: Generate student reports and transcripts
- **Academic Session Management**: Manage academic years and semesters

### 👨‍🏫 Teacher Features
- **Class Management**: View assigned courses and students
- **Material Upload**: Upload study materials, notes, and assignments
- **Attendance Tracking**: Mark and manage student attendance
- **Grade Management**: Enter and update student grades
- **Communication**: Make announcements and provide feedback to students

### 👨‍🎓 Student Features
- **Profile Management**: View and update personal profile information
- **Course Registration**: Browse and register for available courses
- **Resource Access**: Access course materials and assignments
- **Academic Tracking**: Check attendance records and view grades
- **Transcript Download**: Download academic transcripts

## 🎨 User Interface

The system features a clean, professional interface inspired by the Chrix Tech Academic portal:

- **Clean Layout**: Simple, uncluttered design with professional appearance
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices  
- **Intuitive Navigation**: Clear sidebar menu with easy access to all features
- **Consistent Styling**: Uniform appearance across all sections and pages
- **Accessibility**: Easy-to-read fonts, proper contrast, and keyboard navigation support

### Course Management Interface
- **Overview**: Course information, statistics, and recent activity
- **Announcements**: Clean table view of course announcements
- **Resources**: File management and resource sharing
- **Assignments**: Assignment creation and submission tracking
- **Gradebook**: Grade management and analytics
- **Discussions**: Forum-style discussions and Q&A
- **Tests & Quizzes**: Online assessment tools
- **Drop Box**: File submission and sharing
- **Chat Room**: Real-time communication
- **Email Archive**: Message history and communication
- **Roster**: Student management and class lists
- **Calendar**: Schedule and event management
- **Help**: System documentation and support

## 🛠️ Technology Stack

- **Backend**: Django 4.2+ (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Authentication**: Django Auth with role-based access control
- **File Handling**: Django FileField for document uploads
- **Forms**: Django Crispy Forms with Bootstrap styling

## 📋 System Requirements

- Python 3.8+
- Django 4.2+
- Bootstrap 5
- Font Awesome 6

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Academic\ student
```

### 2. Install Dependencies
```bash
pip install django django-crispy-forms crispy-bootstrap4 pillow
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Create Demo Users (Optional)
```bash
python manage.py create_demo_users
```

**Login Credentials:**

**Admin Access:**
- Username: `admin`
- Password: Set during superuser creation

**Student Demo Account:**
- Student ID: `STU001`
- Password: `student123`

**Teacher Demo Account:**
- Employee ID: `EMP001` 
- Password: `teacher123`

### 6. Run Development Server
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`

## 📁 Project Structure

```
Academic student/
├── sams/                   # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User management app
│   ├── models.py          # Profile, Student, Teacher models
│   ├── views.py           # Authentication & user management
│   ├── forms.py           # User registration forms
│   └── admin.py           # Admin interface configuration
├── courses/                # Course management app
│   ├── models.py          # Course, Section, Enrollment models
│   ├── views.py           # Course-related views
│   └── admin.py           # Course admin interface
├── grades/                 # Grade management app
│   ├── models.py          # Grade, Assignment submission models
│   ├── views.py           # Grading views
│   └── admin.py           # Grade admin interface
├── attendance/             # Attendance tracking app
│   ├── models.py          # Attendance, Session models
│   ├── views.py           # Attendance views
│   └── admin.py           # Attendance admin interface
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── accounts/          # User-related templates
│   ├── courses/           # Course templates
│   ├── grades/            # Grade templates
│   └── attendance/        # Attendance templates
├── static/                 # Static files
│   └── css/
│       └── style.css      # Custom styles
└── media/                  # User uploaded files
```

## 🔐 User Roles & Permissions

### Administrator
- Full system access
- User management (students, teachers)
- Course and section management
- System configuration
- Report generation

### Teacher
- View assigned sections
- Manage course materials
- Mark attendance
- Grade students
- View student information

### Student
- View personal dashboard
- Access enrolled courses
- View grades and attendance
- Download transcripts
- Update profile information

## 🎨 UI/UX Features

### Responsive Design
- Mobile-friendly interface
- Bootstrap 5 responsive grid system
- Cross-browser compatibility (Chrome, Firefox, Edge)

### User Experience
- Role-based dashboards with user type selection
- Modern login interface with Student/Staff differentiation
- Intuitive navigation with contextual menus
- Real-time notifications and feedback messages
- Search and filter functionality
- Clean and professional interface design

### Accessibility
- Font Awesome icons for better visual cues
- Consistent color scheme
- Clear typography
- Keyboard navigation support

## 🔧 Configuration

### Database Configuration
For production, update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sams_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files Configuration
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

### Media Files Configuration
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 📊 Database Models

### Core Models

#### Profile Model
- Links to Django User model
- Stores role (Admin/Teacher/Student)
- Personal information (phone, address, DOB)
- Profile picture

#### Student Model
- Student-specific information
- Student ID and registration number
- Admission and graduation dates
- Academic status

#### Teacher Model
- Teacher-specific information
- Employee ID and department
- Qualifications and experience
- Join date and status

#### Course & Section Models
- Course information (code, name, credits)
- Section management (teacher assignment, schedule)
- Enrollment tracking
- Prerequisites handling

## 🚦 Getting Started

### First Time Setup

1. **Access Admin Panel**: `http://127.0.0.1:8000/admin`
2. **Create Academic Year**: Add current academic year
3. **Create Semester**: Add current semester
4. **Add Courses**: Create course catalog
5. **Add Teachers**: Register teaching staff
6. **Add Students**: Register student body
7. **Create Sections**: Assign teachers to course sections

### Sample Data Creation

Use Django admin interface to create:
- Academic years and semesters
- Course catalog with prerequisites
- Teacher profiles with departments
- Student profiles with IDs
- Course sections with schedules

## 🔄 Development Status

### ✅ Completed Features
- User authentication and authorization
- Role-based access control
- Basic dashboard interfaces
- Database models and migrations
- Admin interface configuration
- Responsive UI framework

### 🚧 In Development
- Course enrollment system
- Grading interface
- Attendance marking system
- Material upload functionality
- Assignment submission system
- Report generation

### 📝 Planned Features
- Email notifications
- Calendar integration
- Advanced reporting
- Student transcript generation
- Bulk operations
- Data export/import
- Mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🙏 Acknowledgments

- Django Framework Community
- Bootstrap Team
- Font Awesome
- Educational institutions providing requirements feedback

---

**SAMS** - Streamlining Academic Management for Educational Excellence