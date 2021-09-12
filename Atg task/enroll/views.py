from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, EditUserProfileForm ,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
     


# Create your views here.
#sign_up can be any name here...
def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        print('yaha se->',request.POST, '<-this is post')
        if fm.is_valid():
            messages.success(request, 'Account has been created succesfully')
            fm.save()
    else:
        fm=SignUpForm()
    
    return render(request, 'enroll/signup.html' , {'form': fm})

#login view fuction
def user_login(request):
    #if user is authenticated then this 'if' will be 'false' this means user is already authenticated, then it will redirect us to profile, if we will try to manually put '/login' when we are in our profile page.
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request, user)
                    #after successfull login it will redirect to profile url.
                    #this message will passed to that html page wherever redirect takes us , in this case this message we will get into profile.html because redirect('/profile/)
                    #this message will show only once in profile.html
                    messages.success(request, ' succesfully login to your profile')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()

        return render(request,'enroll/userlogin.html',{'form':fm})
    
    else:
        return HttpResponseRedirect('/profile/')


# profile
def user_profile(request):
    #this is possible that some user can manually type '/profile' url ,although they will treat like a anonymous user.
    #so to prevent going directly into url /profile. we need to check, that is user authenticated or not , if not it will redirect it to the login page
    if request.user.is_authenticated:
        if request.method == "POST":
            #this else part is to handle POST request for user profile.
            #but what if admin will login here, for that situation we require to show almost all fields to him
            #for this , we will pass the class EditAdminProfileForm which we have created for our admin in forms.py
            #first, we will check wheather user is super user or common user
            if request.user.is_superuser == True:
                
                #if also passing users object here so that our super user can see data of others user
                users = User.objects.all()
                fm = EditAdminProfileForm(request.POST,instance=request.user)

            #else it will pass fields that we defined in our EditAdminProfileForm
            else:
                # to show user information we are creating object fm and passing current user information to it and then we're passing that into our template.
                fm = EditUserProfileForm(request.POST,instance=request.user)
                #users = None , so that we can avoid 'call before assign' error see video 68 , skip to 23:18
                users = None

            if fm.is_valid():
                messages.success(request, 'profile updated successfully.')
                fm.save()


        else:
            #this else part is to handle GET request for user profile
            #but what if admin will login here, for that situation we require to show almost all fields to him
            #for this , we will pass the class EditAdminProfileForm which we have created for our admin in forms.py
            #first, we will check wheather user is super user or common user
            if request.user.is_superuser == True:
                #if also passing users object here so that our super user can see data of others user
                users = User.objects.all()
                fm = EditAdminProfileForm(instance=request.user)

            #else it will pass fields that we defined in our EditAdminProfileForm
            else:
                # to show user information we are creating object fm and passing current user information to it and then we're passing that into our template.
                fm = EditUserProfileForm(instance=request.user)
                #users = None , so that we can avoid 'call before assign' error see video 68 , skip to 23:18
                users = None

        return render(request,'enroll/profile.html' , {'name': request.user , 'form':fm , 'users':users})
    else:
        return HttpResponseRedirect('/login/')


# logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# Change Password with old password
def user_change_pass(request):
    #if user is authenticated then only user can see this view template, otherwise it will redirected to login page.
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                #after saving it will redirect to profile.
                #but it will redirect us to logout, to prevent this we will update_session to maintain session
                update_session_auth_hash(request, fm.user)

                #after updating it will show us this message into our profile.
                messages.success(request, 'password Changed Successfully')
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request,'enroll/changepass.html',{'form':fm})
    
    else:
        return HttpResponseRedirect('/login/')

#user detail for admin
def user_detail(request,id):
    if request.user.is_authenticated:
#pi is usergiven(primary id)     #pk = primary key
        pi = User.objects.get(pk=id)
        #taking admin profile form , so that we can see all the fields of user
        fm = EditAdminProfileForm(instance=pi)
        return render(request, 'enroll/userdetail.html',{'form': fm})
    else:
        return HttpResponseRedirect('/login/')