from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from userauths.models import Profile, User
from userauths.forms import UserRegisterForm 
from core.models import Post

def registerView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are registered!")
        return redirect("core:feed")
    
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get("full_name")
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")

        user = authenticate(email=email, password=password)
        login(request, user)

        messages.success(request, f"Hi {full_name}, your account was created successfully!")

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone

        profile.save()

        return redirect("core:feed")
    
    context = {
        "form" : form
    }

    return render(request, "userauths/sign-up.html", context)

def loginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are registered!")
        return redirect("core:feed")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in!")
                return redirect("core:feed")
            else:
                messages.warning(request, "Username or password does not match!")
                return redirect("userauths:sign-up")
        except:
            messages.warning(request, "User does not exist!")
            return redirect("userauths:sign-up")
        
    return HttpResponseRedirect("/")

def logoutView(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect("userauths:sign-up")

@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(active=True, user=request.user).order_by("-id")

    context = {
        "profile" : profile,
        "posts" : posts,
    }

    return render(request, "userauths/my-profile.html", context)


@login_required
def friend_profile(request, username):
    profile = Profile.objects.get(user__username=username)
    posts = Post.objects.filter(active=True, user=profile.user).order_by("-id")

    context = {
        "profile" : profile,
        "posts" : posts,
    }

    return render(request, "userauths/friend-profile.html", context)
