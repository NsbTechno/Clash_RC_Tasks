from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import extendeduser
import re


def login(request):
    page = 'login'
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['pass'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login_Signup.html', {'error': "Invaild Crededntials"})
    else:
        return render(request, 'users/login_Signup.html')


def register(request):
    page = 'register'
    context = {'page': page}
    if request.method == 'POST':

        if request.POST['pass'] == request.POST['passwordagain']:
            try:
                user = User.objects.get(username=request.POST['username'])
                messages.error(request, 'An ERROR OCUUERRR')
                return redirect('register')
            except User.DoesNotExist:
                first_name = request.POST['fn']
                last_name = request.POST['ln']
                email = request.POST['email']
                phnum = request.POST['phone']

            if (len(request.POST['pass'])<8):
                    return render(request,'users/login_Signup.html',{'error':"Password too Short, Should Contain ATLEAST 1 Uppercase,1 lowercase,1 special Character and 1 Numeric Value"})

            elif not re.search(r"[\d]+",request.POST['pass']):
                    return render(request,'users/login_Signup.html',{'error':"Your Password must contain Atleast 1 Numeric "})

            elif not re.findall('[A-Z]', request.POST['pass']):   
                     return render(request,'users/login_Signup.html',{'error':"Your Password must contain Atleast 1 UpperCase Letter "})

            elif not re.findall('[a-z]',request.POST['pass']):
                    return render(request,'users/login_Signup.html',{'error':"Your Password must contain Atleast 1 lowercase Letter "})
                    
            elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', request.POST['pass']):   
                     return render(request,'users/login_Signup.html',{'error':"Your Password must contain Atleast 1 Specail character "})     

            else:
                    if extendeduser.objects.filter(email=email):
                        return render(request,'users/login_Signup.html',{'error':"Email Already  Registered  "})
                    elif extendeduser.objects.filter(phone_num=phnum):
                        return render(request,'users/login_Signup.html',{'error':"Phone Number Already Registered"})

                    else:
                        user = User.objects.create_user(username=request.POST['username'], password=request.POST['pass'])
                        newextendeduser = extendeduser(first_name=first_name, last_name=last_name, email=email, phone_num=phnum, user=user)
                        newextendeduser.save()
                        auth.login(request, user)
                    messages.success(
                        request, f'Your account has been Create!! Login Now')
                    return redirect('login')
        else:
            return render(request, 'users/login_Signup.html', {'error': "Password and Confirm Password Doesnt Match"})

    else:
        return render(request, 'users/login_Signup.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User Logged Out!!!!!!')
    return redirect('login')



@login_required(login_url='login')
def profile(request):
    datas = extendeduser.objects.filter(user = request.user)
    return render(request,'users/profile.html',{'data':datas})




