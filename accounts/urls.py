from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Password Reset URLs
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset_password'),
    
    # Settings
    path('settings/', views.settings_view, name='settings'),
    
    # Pin/Unpin functionality
    path('toggle-pin/', views.toggle_pin_view, name='toggle_pin'),
    
    # Profile editing URLs
    path('profile/edit/basic/', views.edit_basic_information, name='edit_basic_info'),
    path('profile/edit/pronunciation/', views.edit_name_pronunciation, name='edit_name_pronunciation'),
    path('profile/edit/contact/', views.edit_contact_information, name='edit_contact_info'),
    path('profile/edit/student/', views.edit_student_information, name='edit_student_info'),
    path('profile/edit/staff/', views.edit_staff_information, name='edit_staff_info'),
    path('profile/picture/change/', views.change_profile_picture, name='change_profile_picture'),
    path('profile/picture/delete/', views.delete_profile_picture, name='delete_profile_picture'),
    path('profile/status/update/', views.update_status, name='update_status'),
    
    # Admin URLs
    path('admin/students/', views.manage_students_view, name='manage_students'),
    path('admin/teachers/', views.manage_teachers_view, name='manage_teachers'),
    path('admin/add-student/', views.add_student_view, name='add_student'),
    path('admin/add-teacher/', views.add_teacher_view, name='add_teacher'),
]