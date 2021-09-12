from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import widgets
from django import forms

#this signUpForm is given by me.
class SignUpForm(UserCreationForm):
    #we can not change password label the way we were changing 'Email' given below
    #to change password label we need to override the django code this way..
    #password1 is password field and password2 is re-password field in django.
    password1 = forms.CharField(label='Enter Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Enter Password(again)',widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username' ,'first_name','last_name','email']
        #django define all the label, to make changes in defult labels we can do in this way..
        #django defult label for email field is 'Email Address' 
        #now label changed to "Email Account".
        labels = {'email':'Email Account'}

        
class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name' , 'last_name', 'email', 'date_joined', 'last_login']
        #changing email label because it will show us 'Email address' as defualt label
        labels = {'email' : 'Email'}
        
class EditAdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'
        #changing email label because it will show us 'Email address' as defualt label
        labels = {'email' : 'Email'}