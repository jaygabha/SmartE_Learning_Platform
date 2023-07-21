from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import RegistrationForm, PaymentForm, LoginForm, AddCourseForm, AddChapterForm, AddContentForm
from django.contrib.auth.models import User

from .models import Membership, Student, Courses, Professor, FilesStorage, CourseModules


def professor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='Professor').exists():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print(request.user.groups.count())
        if not request.user.is_authenticated or request.user.groups.count() != 0:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


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
                if user_type == 'Student':
                    login(request, user)
                    return redirect('SmartE_app:course_list')  # Redirect to student dashboard
                elif user_type == 'Professor':
                    login(request, user)
                    if user.groups.filter(name='Professor').exists():
                        return redirect('SmartE_app:course_dashboard')  # Redirect to teacher dashboard
                    else:
                        return render(request, 'SmartE_app/login.html', {'form': form, 'error_message': 'Invalid User'})
    else:
        form = LoginForm()

    return render(request, 'SmartE_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('SmartE_app:login')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            sid = form.cleaned_data['sid']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            membership_type = form.cleaned_data['membership_type']

            user = User.objects.create_user(username=username, password=password)
            user.email = email
            user.first_name = name
            user.save()

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

@professor_required
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

@professor_required
def course_detail(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)

    if request.method == 'POST':
        chapter_form = AddChapterForm(request.POST, request.FILES)

        if chapter_form.is_valid():
            chapter = chapter_form.save(commit=False)
            chapter.course = course
            chapter.save()

            # Associate content with the chapter


            # Save the chapter content first
            chapter.save()

            # Handle file upload manually and associate files with the chapter
            files = request.FILES.getlist('files')
            for file in files:
                file_obj = FilesStorage(module=chapter, file=file)
                file_obj.save()

            return redirect('SmartE_app:course_dashboard')

    else:
        chapter_form = AddChapterForm()

    context = {
        'course': course,
        'chapter_form': chapter_form,
    }
    return render(request, 'SmartE_app/course_detail.html', context)

# views.py

# ...

@professor_required
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

@professor_required
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

@student_required
def course_list(request):

    #student = Student.objects.filter(sid=request.user.sid).first()
    #print(student.sid)
    #print(Student.objects.filter(sid__in=User.objects.filter(username=request.user.username)))
    courses = Courses.objects.all()
    return render(request, 'SmartE_app/course_list.html', {'courses': courses})

@student_required
def course_detail_student(request, course_id):
    course = CourseModules.objects.filter(course=course_id)
    return render(request, 'SmartE_app/course_detail_student.html', {'course': course, 'course_id': course_id})