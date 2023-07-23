from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import RegistrationForm, PaymentForm, LoginForm, AddCourseForm, AddChapterForm, AddContentForm, AddAttendanceForm, QuizForm, QuestionForm, AnswerForm
from django.contrib.auth.models import User

from .models import Membership, Student, Courses, Professor, FilesStorage, CourseModules, Attendance, ModuleProgress, \
    Quiz, Question, Answer


def check_access_level(student_mem, course_mem):
    types = {
        "bronze": 1,
        "silver": 2,
        "gold": 3,
    }
    if types[student_mem]>= types[course_mem]:
        return True
    return False
def professor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='Professor').exists():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
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
                messages.error(request, 'Invalid Username or Password')
                return redirect('SmartE_app:login')
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

            user = Student.objects.create_user(username=username, password=password, sid=sid,
                                               membership=membership_type)
            user.email = email
            user.first_name = name
            user.save()

            return redirect('SmartE_app:payment')  # Redirect to a success page
    else:
        form = RegistrationForm()

    return render(request, 'SmartE_app/registration.html', {'form': form})


def payment(request):
    try:
        student = Student.objects.get(id=request.user.id)
        membership = str(student.membership.type).title()
        price = student.membership.price
    except Exception:
        return render(request, 'SmartE_app/payment.html', {'msg': "User not registered. Please register before"})
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # membership_type = form.cleaned_data['membership_type']
            name = form.cleaned_data['name']
            cardnumber = form.cleaned_data['cardnumber']
            expiry = form.cleaned_data['expiry']
            cvv = form.cleaned_data['cvv']

            # Additional logic to process payment or display price
            # Example:
            if True:
                # Process the payment and update the necessary records
                # ...
                return render(request, 'SmartE_app/payment_success.html', {'message': "Payment is Successful"})


    else:
        form = PaymentForm()

    return render(request, 'SmartE_app/payment.html', {'form': form, 'price': price, "mem_type": membership})


@professor_required
def professor_dashboard(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            professors = form.cleaned_data["professors"]
            for professor in professors:
                if not professor.groups.filter(name='Professor').exists():
                    return render(request, 'SmartE_app/professor_dashboard.html', {"msg": "The user selected is not a professor"})
            form.save()
            # Redirect to a success page or the course detail page
            return redirect('SmartE_app:course_detail', course_id=form.cleaned_data["course_id"])
    else:
        form = AddCourseForm()

    context = {
        'form': form,
    }
    return render(request, 'SmartE_app/professor_dashboard.html', context)
##Parul
# @professor_required
# def manage_courses(request):
#     courses = Courses.objects.filter(professors=request.user.professors)
#     return render(request, 'manage_courses.html', {'courses': courses})

@professor_required
def create_quiz(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    if request.method == 'POST':
        form = QuizForm(request.POST)
       # formset = QuestionFormSet(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()

            # questions = formset.save(commit=False)
            # for question in questions:
            #     question.quiz = quiz
            #     question.save()

            return redirect('SmartE_app:course_dashboard')
    else:
        form = QuizForm()
        #formset = QuestionFormSet()

    context = {
        'course': course,
        'form': form,
        # 'formset': formset
    }
    return render(request, 'SmartE_app/create_quiz.html', context)

@professor_required
def add_question(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('SmartE_app:quiz_detail', course_id=course_id, quiz_id=quiz.id)
    else:
        form = QuestionForm()
    context = {
        'quiz': quiz,
        'form': form,
    }
    return render(request, 'SmartE_app/add_question.html', context)

@professor_required
def question_detail(request, course_id, quiz_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()  # Get all answers related to this question

    context = {
        'course_id': course_id,
        'quiz_id': quiz_id,
        'question': question,
        'answers': answers,
    }
    return render(request, 'SmartE_app/question_detail.html', context)

@professor_required
def add_answer(request, course_id, quiz_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('SmartE_app:question_detail', course_id=course_id, quiz_id=quiz_id, question_id=question_id)
    else:
        form = AnswerForm()
    context = {
        'question': question,
        'form': form,
        'course_id': course_id,
        'quiz_id': quiz_id,
        'question_id': question_id,
    }
    return render(request, 'SmartE_app/add_answer.html', context)


def quiz_detail(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Get all questions related to this quiz

    context = {
        'course_id': course_id,  # Ensure this is being passed in
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'SmartE_app/quiz_detail.html', context)


# @professor_required
# def delete_quiz(request, course_id, quiz_id):
#     quiz = get_object_or_404(Quiz, id=quiz_id)
#     if request.method == 'POST':
#         quiz.delete()
#         return redirect('SmartE_app:course_dashboard')
#     else:
#         context = {
#             'quiz': quiz,
#         }
#         return render(request, 'SmartE_app/confirm_delete_quiz.html', context)


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

        # Query quizzes for the course
        quizzes = course.quiz_set.all()
        course_quizzes = []
        for quiz in quizzes:
            quiz_detail_url = reverse('SmartE_app:quiz_detail', args=[course.course_id, quiz.id])
            course_quizzes.append({
                'quiz_name': quiz.name,
                'quiz_id': quiz.id,
                'quiz_url': quiz_detail_url,  # add quiz detail URL
            })

        # Add edit, delete and create quiz URLs for each course
        course_edit_url = reverse('SmartE_app:course_detail', args=[course.course_id])
        course_delete_url = reverse('SmartE_app:course_delete', args=[course.course_id])
        course_quiz_url = reverse('SmartE_app:create_quiz', args=[course.course_id])
        course_data.append({
            'course': course,
            'modules': course_modules,
            'quizzes': course_quizzes,
            'edit_url': course_edit_url,
            'delete_url': course_delete_url,
            'add_quiz' : course_quiz_url,
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

    student_user = Student.objects.get(username=request.user.username)

    # Try to get the ModuleProgress instance for the student and module
    try:
        module_progress = ModuleProgress.objects.get(student=student_user, module=chapter)
    except ModuleProgress.DoesNotExist:
        # If the ModuleProgress instance doesn't exist, create a new one
        module_progress = ModuleProgress(student=student_user, module=chapter, viewed=False)

    # Mark the module as viewed (set the 'viewed' field to True)
    module_progress.viewed = True
    module_progress.save()
    return render(request, 'SmartE_app/module_detail.html', context)


@student_required
def course_list(request):
    student_user = Student.objects.get(username=request.user.username)
    student_membership = student_user.membership
    membership_type = student_membership.type
    q1 = Courses.objects.filter(membership_access_level__type="bronze")
    courses = q1
    if membership_type == "silver":
        q2 = Courses.objects.filter(membership_access_level__type="silver")
        courses = q2.union(q1)
    elif membership_type == "gold":
        q2 = Courses.objects.filter(membership_access_level__type="silver").union(q1)
        q3 = Courses.objects.filter(membership_access_level__type="gold")
        courses = q3.union(q2)

    for course in courses:
        # Get the modules that belong to this course
        course_modules = course.coursemodules_set.all()

        # Calculate the total number of modules for this course
        total_modules = course_modules.count()

        # Calculate the total number of modules viewed by the student for this course
        total_modules_viewed = ModuleProgress.objects.filter(student=student_user, module__in=course_modules).count()

        # Calculate the percentage of total modules viewed
        if total_modules > 0:
            percentage_modules_viewed = (total_modules_viewed / total_modules) * 100
        else:
            percentage_modules_viewed = 0

        # Store the percentage in the course object
        course.percentage_completed = percentage_modules_viewed
    return render(request, 'SmartE_app/course_list.html', {'courses': courses})


@student_required
def course_detail_student(request, course_id):
    course = CourseModules.objects.filter(course=course_id)
    return render(request, 'SmartE_app/course_detail_student.html', {'course': course, 'course_id': course_id})


@login_required
def attendance(request):
    if not request.user.is_authenticated:
        return render(request, 'SmartE_app/attendance.html', {'msg': "User is not authenticated", "Professor": False})
    # try:
    if request.user.groups.filter(name='Professor').exists():
        courses = Courses.objects.filter(professors=request.user).order_by("name")
        return render(request, 'SmartE_app/attendance.html',{ 'courses': courses, "Professor": True })
    elif request.user.groups.count() == 0:
        std = Student.objects.get(username=request.user.username)
        q1 = Courses.objects.filter(membership_access_level__type="bronze")
        courses = q1
        if std.membership.type == "silver":
            q2 = Courses.objects.filter(membership_access_level__type="silver")
            courses = q2.union(q1)
        elif std.membership.type == "gold":
            q2 = Courses.objects.filter(membership_access_level__type="silver").union(q1)
            q3 = Courses.objects.filter(membership_access_level__type="gold")
            courses = q3.union(q2)

        attendance_list = []
        for course in courses:
            try:
                att = Attendance.objects.get(student=std, course=course)
                temp = {"percentage": att.attendance_percentage()}
                temp["course_id"] = att.course.course_id
                temp["couse_name"] = att.course.name
                attendance_list.append(temp)
            except Exception:
                pass


        return render(request, 'SmartE_app/attendance.html',{'attendance_list': attendance_list, "Professor": False })
    else:
        return render(request, 'SmartE_app/attendance.html',
                      {'msg': "User is not a student or professor. For admins Please use Django admin", "Professor": False})
    # except Exception as e:
    #     return render(request, 'SmartE_app/attendance.html', {'msg': str(e), "Professor": False})

@professor_required
def add_attendance(request, course_id):
    form = AddAttendanceForm()
    msg = ""
    try:
        course = Courses.objects.get(course_id=course_id)
        if request.user.username not in course.professors.all().values_list('username', flat=True):
            return render(request, 'SmartE_app/add_attendance.html',{'msg': "Unauthorized to view this course"})
    except Exception:
            return render(request, 'SmartE_app/add_attendance.html', {'msg': "Invalid Course ID"})
    if request.method == "POST":
        filled_form = AddAttendanceForm(request.POST)
        if filled_form.is_valid():
            student = filled_form.cleaned_data["student"]
            if not check_access_level(student.membership.type, course.membership_access_level.type):
                msg = "Student not have necessary membership."
            else:
                try:
                    att = Attendance.objects.get(student=student, course=course)
                    att.attendance[filled_form.cleaned_data["week"]] = filled_form.cleaned_data["present"]
                    att.save()
                except Exception:
                    attendance = {filled_form.cleaned_data["week"]: filled_form.cleaned_data["present"]}
                    Attendance.objects.create(student=student, course=course, attendance=attendance)
        else:
            return render(request, 'SmartE_app/add_attendance.html', {'msg': "Invalid Form"})
    att = Attendance.objects.filter(course=course)
    attendance_list = []
    for item in att:
        temp = {"percentage": item.attendance_percentage()}
        temp["student_username"] = item.student.username
        temp["student_name"] = item.student.get_full_name()
        attendance_list.append(temp)

    return render(request, 'SmartE_app/add_attendance.html',
                      {'form': form, 'course_id': course.course_id, "course_name": course.name, "attendance_list": attendance_list,  "msg": msg})


def quiz_detail_student(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    context = {
        'quiz': quiz,
        'questions': questions,
    }

    return render(request, 'SmartE_app/quiz_detail_student.html', context)
def course_quiz_list(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    quizzes = Quiz.objects.filter(course=course)

    context = {
        'course': course,
        'quizzes': quizzes,
    }

    return render(request, 'SmartE_app/course_quiz_list.html', context)

def submit_quiz(request, course_id, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        total_questions = questions.count()
        correct_answers = 0

        # Process the student's answers
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                answer = get_object_or_404(Answer, id=answer_id)
                if answer.is_correct:
                    correct_answers += 1

        # Calculate the quiz score
        score = (correct_answers / total_questions) * 100

        context = {
            'quiz': quiz,
            'score': score,
        }

        return render(request, 'SmartE_app/quiz_response.html', context)

    return redirect('SmartE_app:quiz_detail', course_id=course_id, quiz_id=quiz_id)