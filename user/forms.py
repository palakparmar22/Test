from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Questions, Contactus, User_Details, Job,  JOB_CHOICES, DEPARTMENT_CHOICES, ROLE_CHOICES


class ResumeForm(forms.ModelForm):
    class Meta:
        model = User_Details
        fields = ['res']
    

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    usable_password = None
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contactus
        fields = ['name', 'email', 'msg']
        labels = {
            'msg': "Message"
        }
        widgets = {
            'name' : forms.TextInput(attrs={"class":"form-control"}),
            'email' : forms.EmailInput(attrs={"class":"form-control"}),
            'msg' : forms.TextInput(attrs={"class":"form-control", "rows":"5"})
        }




class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'department', 'description', 'requirements']
        widgets = {
            'department': forms.TextInput(attrs={'class':'form-control', 'id':'departid'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'id':'descid'}),
            'requirements': forms.Textarea(attrs={'class':'form-control', 'id':'reqrid'}),
        }

    title = forms.ChoiceField(choices=JOB_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'id':'titleid'}))
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'id':'departid'}))

