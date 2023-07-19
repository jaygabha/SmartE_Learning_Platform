from django import forms
from .models import Membership, Courses, FilesStorage, CourseModules
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
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
    membership_type = forms.ModelChoiceField(queryset=Membership.objects.all())
    name = forms.CharField(max_length=100)
    cardnumber = CardNumberField(label='Card Number')
    expiry = CardExpiryField(label='Expiration Date')
    cvv = SecurityCodeField(label='CVV/CVC')

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