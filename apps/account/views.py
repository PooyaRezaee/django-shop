from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from .mixins import NoLoginMixin
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import User


class RegisterView(NoLoginMixin, View):
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "account/register.html",{"form":form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(email=data["email"],password=data["password"])
                print("Successfly created")
                return redirect(reverse("main:home"))
            except IntegrityError:
                print("This email has already been registered.")
        print(form.errors)
        return render(request,"account/register.html",{"form":form})


class CustomLoginView(NoLoginMixin, View):
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request,"account/login.html",{"form":form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, email=data["email"], password=data["password"])
            if user is not None:
                login(request,user)
                print('You Logged')
                return redirect('main:home')
            else:
                print('UserName or Password Is Wrong')
        
        print(form.errors)
        return render(request,"account/login.html",{"form":form})

class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        print('You Logouted')
        return redirect('main:home')
from django.contrib import messages


class UpdateProfileView(LoginRequiredMixin,View):
    form_class = ProfileForm

    def get(self,request):
        form = self.form_class(instance=request.user)

        return render(request,"account/profile.html",{"form":form})

    def post(self,request):
        if request.POST.get('email') != request.user.email:
            # messages.error(request, "You don't have access to change email.")
            print("Email changed")
            return redirect('account:profile')
        
        form = self.form_class(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            print("Form updated")
            return redirect(reverse("main:home"))

        return render(request,"account/profile.html",{"form":form})
