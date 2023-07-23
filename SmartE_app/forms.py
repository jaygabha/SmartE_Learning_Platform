from django import forms
from .models import Membership, Courses, FilesStorage, CourseModules, Attendance, Student, Quiz, Question, Answer
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from multiupload.fields import MultiFileField
#from django.forms.models import inlineformset_factory


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('Student', 'Student'), ('Professor', 'Professor')))

class RegistrationForm(forms.Form):
    sid = forms.CharField(max_length=10)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    membership_type = forms.ModelChoiceField(queryset=Membership.objects.all())

class PaymentForm(forms.Form):
    # membership_type = forms.ModelChoiceField(queryset=Membership.objects.all())
    name = forms.CharField(max_length=100)
    cardnumber = forms.IntegerField(min_value=100000000000, max_value=9999999999999999999)
    expiry = CardExpiryField(label='Expiration Date')
    cvv = SecurityCodeField(label='CVV/CVC')
class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_id', 'name', 'membership_access_level', 'professors']
##Parul
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'course']
    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']


class AddChapterForm(forms.ModelForm):
    files = MultiFileField(min_num=1, max_num=5)
    class Meta:
        model = CourseModules
        fields = ['module_name', 'content','files']

class AddContentForm(forms.ModelForm):
    class Meta:
        model = CourseModules
        fields = ['module_name', 'content']


class AddAttendanceForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    week = forms.IntegerField(min_value=1)
    Choices = [(True, True),(False,False)]
    present = forms.ChoiceField(choices=Choices)
