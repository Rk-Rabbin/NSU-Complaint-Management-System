from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm, PasswordResetForm
from django.utils.translation import gettext, gettext_lazy as _
from .models import Student, User, Faculty, Employee, Complaint
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

position = (
    ('admin','admin'),
    ('Student','Student'),
    ('Faculty','Faculty'),
    ('Employee','Employee')
)
class RegistrationForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields =['name', 'email', 'position', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
    'class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
    'autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}),help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email',
    'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}),help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}))

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','student_id']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                    'student_id':forms.TextInput(attrs={'class':'form-control'})}

class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name','faculty_initial']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                    'faculty_initial':forms.TextInput(attrs={'class':'form-control'})}

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','employee_id','sector']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                    'employee_id':forms.TextInput(attrs={'class':'form-control'}),
                    'sector':forms.Select(attrs={'class':'regDropDown'})}

# fac = Complaint.objects.get(position="Faculty")
# reviewer = (
#     ('faculty','fac')
# )
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        # exclude = ('reviewer',)
        fields = ['complainer', 'accused','accused_status','reviewer','statement','upload']
        widgets = {'complainer':forms.TextInput(attrs={'class':'form-control'}),
                    'accused':forms.TextInput(attrs={'class':'form-control'}),
                    'accused_status':forms.Select(attrs={'class':'regDropDown'}),
                    'reviewer':forms.TextInput(attrs={'class':'form-control'}),
                    'statement':forms.Textarea(attrs={'class':'form-control'}),
                    'upload':forms.FileInput(attrs={'class':'form-control'}),
                    }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ('complainer', 'accused','accused_status','statement','upload','reviewer')
        fields = ['reviewer','status','comment']
        widgets = {'status':forms.Select(attrs={'class':'regDropDown'}),
                    'reviewer':forms.TextInput(attrs={'class':'form-control'}),
                    'comment':forms.Textarea(attrs={'class':'form-control'}),
                    }

class ChangeReviewerForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ('complainer', 'accused','accused_status','statement','upload')
        fields = ['reviewer','status','comment']
        widgets = {'status':forms.Select(attrs={'class':'regDropDown'}),
                    'reviewer':forms.TextInput(attrs={'class':'form-control'}),
                    'comment':forms.Textarea(attrs={'class':'form-control'}),
                    }