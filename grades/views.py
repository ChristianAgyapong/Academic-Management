from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def student_grades_view(request):
    # Placeholder - implement student grades view
    return render(request, 'grades/student_grades.html', {})

@login_required
def transcript_view(request):
    # Placeholder - implement transcript view
    return render(request, 'grades/transcript.html', {})

@login_required
def teacher_grading_sections_view(request):
    # Placeholder - implement teacher grading sections view
    return render(request, 'grades/teacher_grading_sections.html', {})

@login_required
def grade_students_view(request, section_id):
    # Placeholder - implement grade students view
    messages.info(request, 'Grading feature coming soon!')
    return redirect('grades:teacher_grading_sections')

@login_required
def grade_assignments_view(request, section_id):
    # Placeholder - implement grade assignments view
    messages.info(request, 'Assignment grading feature coming soon!')
    return redirect('grades:teacher_grading_sections')

@login_required
def assignment_submissions_view(request, assignment_id):
    # Placeholder - implement assignment submissions view
    return render(request, 'grades/assignment_submissions.html', {})
