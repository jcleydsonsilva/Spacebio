from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User



def signin(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')


    page = 'signin'
    return render(request, 'accounts/signin.html', {'page' : page})



def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        myuser = User.objects.create_user(username, email, password)
        
        myuser.save()

        messages.success(request, 'Your account has been successfully created.')

        return redirect('signin')

    page = 'signup'
    return render(request, 'accounts/signup.html', {'page' : page})


def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')
