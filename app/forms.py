# from django import forms
# from django.core.exceptions import ValidationError

# class Signup_Form(forms.Form):
#     first_name=forms.CharField(label='first name',max_length=100)
#     last_name=forms.CharField(label='last name',max_length=100)
#     username=forms.CharField(label='username',max_length=100)
#     email=forms.EmailField()
#     password1=forms.CharField(widget=forms.TextInput(attrs={"Type":"password"}))
#     password2=forms.CharField(widget=forms.TextInput(attrs={"Type":"password"}))

#     def clean(self):
#         super(Signup_Form,self).clean()

#         un=self.cleaned_data.get('username')  #user name as shortcut UN
#         pass1=self.cleaned_data.get('password1')
#         pass2=self.cleaned_data.get('password2')

#         if len(un)<3:
#             self._errors['username'] = self.error_class([
#                 'Minimum 3 characters required'])
#          # return any errors if found
#         return self.cleaned_data


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='first name', max_length=100)
    last_name = forms.CharField(label='last name', max_length=100)
    username = forms.CharField(label='username', min_length=5, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    def username_clean(self):
        username = self.cleaned_data['username']
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email']
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            # self.cleaned_data['first_name'],
            # self.cleaned_data['last_name']
        )
        user.is_active = False
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class TodoForm(forms.ModelForm):
    class Meta:
        model = TODO
        # fields='__all__'
        exclude = ['user']


class UserImageForm(forms.ModelForm):
    class Meta:
        required_fields = ['image']
        # To specify the model to be used to create form
        model = profile
        # It includes all the fields of model
        exclude = ['user']
