from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import RegistrationForm, PaymentForm, LoginForm, AddCourseForm, AddChapterForm, AddContentForm
from django.contrib.auth.models import User

from .models import Membership, Student, Courses, Professor, FilesStorage, CourseModules


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    if user_type == 'Student':
                        if Student.objects.get(username=username):
                            login(request, user)
                            return redirect('SmartE_app:student_dashboard')  # Redirect to student dashboard
                    elif user_type == 'Professor':
                        if Professor.objects.get(username=username):
                            login(request, user)
                            return redirect('SmartE_app:course_dashboard')  # Redirect to teacher dashboard
                    else:
                        return render(request, 'SmartE_app/login.html', {'form': form, 'error_message': 'Invalid User'})
                except Exception:
                    return render(request, 'SmartE_app/login.html', {'form': form, 'error_message': 'Invalid User'})
            else:
                return render(request, 'SmartE_app/login.html', {'form': form, 'error_message': 'Username or password incorrect'})
    else:
        form = LoginForm()

    return render(request, 'SmartE_app/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'SmartE_app/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('SmartE_app:login')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            sid = form.cleaned_data['sid']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            membership = form.cleaned_data['membership']
            try:
                user1 = Student.objects.get(username=username)
                return render(request, 'SmartE_app/login.html', {'form': form, 'error_message': 'User Already exists. Please Login'})
            except Exception:
                newuser = form.save(commit=False)
                newuser.set_password(form.cleaned_data['password'])
                newuser.save()
                return redirect('SmartE_app:payment')  # Redirect to a success page
    else:
        form = RegistrationForm()

    return render(request, 'SmartE_app/registration.html', {'form': form})
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            membership_type = form.cleaned_data['membership_type']
            name = form.cleaned_data['name']
            cardnumber = form.cleaned_data['cardnumber']
            expiry = form.cleaned_data['expiry']
            cvv = form.cleaned_data['cvv']

            # Additional logic to process payment or display price
            # Example:
            if True:
                # Process the payment and update the necessary records
                # ...

                price = Membership.objects.get(type=membership_type).price
                return render(request, 'SmartE_app/payment_success.html', {'price': price})


    else:
        form = PaymentForm()

    return render(request, 'SmartE_app/payment.html', {'form': form})

@login_required  # This decorator ensures that only authenticated users can access the dashboards
def student_dashboard(request):
    # Add your logic here to retrieve and display student-related data
    return render(request, 'SmartE_app/student_dashboard.html')

@login_required
def professor_dashboard(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            form.save_m2m()  # Save the ManyToManyField relationships (students and professors)

            # Redirect to a success page or the course detail page
            return redirect('SmartE_app:course_detail', course_id=course.course_id)
    else:
        form = AddCourseForm()

    context = {
        'form': form,
    }
    return render(request, 'SmartE_app/professor_dashboard.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)

    if request.method == 'POST':
        chapter_form = AddChapterForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        content_form = AddContentForm(request.POST)

        if chapter_form.is_valid() and content_form.is_valid():
            chapter = chapter_form.save(commit=False)
            chapter.course = course

            # Handle file upload
            if 'files' in request.FILES:
                file = request.FILES['files']
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                chapter.files = fs.url(filename)

            chapter.save()

            # Associate content with the chapter
            content = content_form.cleaned_data['content']
            chapter.content = content
            chapter.save()

            # Redirect to the course dashboard after adding the chapter and content
            return redirect('SmartE_app:course_dashboard')
    else:
        chapter_form = AddChapterForm()
        content_form = AddContentForm()

    context = {
        'course': course,
        'chapter_form': chapter_form,
        'content_form': content_form,
    }
    return render(request, 'SmartE_app/course_detail.html', context)

# views.py

# ...

def course_dashboard(request):
    courses = Courses.objects.all()

    course_data = []
    for course in courses:
        modules = course.coursemodules_set.all()
        course_modules = []
        for module in modules:
            course_modules.append({
                'module_name': module.module_name,
                'module_id': module.id,
            })

        # Add edit and delete URLs for each course
        course_edit_url = reverse('SmartE_app:course_detail', args=[course.course_id])
        course_delete_url = reverse('SmartE_app:course_delete', args=[course.course_id])
        course_data.append({
            'course': course,
            'modules': course_modules,
            'edit_url': course_edit_url,
            'delete_url': course_delete_url,
        })

    context = {
        'course_data': course_data,
    }
    return render(request, 'SmartE_app/course_dashboard.html', context)

def course_delete(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('SmartE_app:course_dashboard')
    context = {
        'course': course,
    }
    return render(request, 'SmartE_app/course_confirm_delete.html', context)


def module_detail(request, course_id, module_id):
    chapter = get_object_or_404(CourseModules, id=module_id)

    context = {
        'chapter': chapter,
    }
    return render(request, 'SmartE_app/module_detail.html', context)
