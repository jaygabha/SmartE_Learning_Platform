from django import forms
from .models import Membership, Courses, FilesStorage, CourseModules


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('Student', 'Student'), ('Professor', 'Professor')))

class RegistrationForm(forms.Form):
    sid = forms.CharField(max_length=10,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Student Id'}))
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}),)
    membership_type = forms.ModelChoiceField(queryset=Membership.objects.all(),widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Your membership type'}))

class PaymentForm(forms.Form):
    membership_type = forms.ModelChoiceField(
        queryset=Membership.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    cardnumber = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'})
    )
    expiry = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'})
    )

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['course_id', 'name', 'membership_access_level']

class AddChapterForm(forms.ModelForm):
    class Meta:
        model = CourseModules
        fields = ['module_name', 'files']

class AddContentForm(forms.ModelForm):
    class Meta:
        model = CourseModules
        fields = ['module_name', 'content']