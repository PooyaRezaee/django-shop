from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.core.exceptions import ObjectDoesNotExist
from .mixins import NoLoginMixin
from .forms import LoginForm, RegisterForm, ProfileForm, AddressForm, ChangePasswordForm
from .models import User, Addresses


class RegisterView(NoLoginMixin, View):
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(
                    email=data["email"], password=data["password"]
                )
                messages.success(request, "You have successfully registered.")
                return redirect(reverse("main:home"))
            except IntegrityError:
                messages.warning(request, "This email has already been registered.")
        else:
            messages.warning(request, "Form not valid.")
        return render(request, "account/register.html", {"form": form})


class CustomLoginView(NoLoginMixin, View):
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, "account/login.html", {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, email=data["email"], password=data["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect("main:home")
            else:
                messages.warning(request, "UserName or Password Is Wrong.")
        else:
            messages.warning(request, "form not valid.")
        return render(request, "account/login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have successfully registered.")
        return redirect("main:home")


class ChangePasswordView(View):
    form_class = ChangePasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, "account/change_password.html", {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if not form.is_valid():
            for field, error in form.errors.items():
                messages.error(request, str(error))

            return redirect(reverse("account:password-change"))

        user = request.user
        cd = form.cleaned_data
        user.set_password(cd["password1"])
        user.save()
        
        messages.success(request, "succesfuly password changed.")
        return redirect(reverse("main:home"))


class UpdateProfileView(LoginRequiredMixin, View):
    form_class = ProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user)

        return render(request, "account/profile.html", {"form": form})

    def post(self, request):
        if request.POST.get("email") != request.user.email:
            messages.error(request, "You don't have access to change email.")
            return redirect("account:profile")

        form = self.form_class(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated")
            return redirect(reverse("main:home"))

        messages.warning(request, "Form not valid.")
        return render(request, "account/profile.html", {"form": form})


class AddresseListView(LoginRequiredMixin, ListView):
    model = Addresses
    context_object_name = "addresses"
    template_name = "address/list.html"

    def check_defualt_address(self):
        if self.request.GET.get("defualt_address"):
            pk_defualt_address = self.request.GET.get("defualt_address")
            user = self.request.user
            try:
                user.default_address = Addresses.objects.get(pk=pk_defualt_address)
                user.save()
            except ObjectDoesNotExist:
                messages.warning(self.request, "address id does not exists.")

    def get_queryset(self):
        self.check_defualt_address()
        return self.model.objects.filter(user=self.request.user)


class AddresseUpdateView(LoginRequiredMixin, UpdateView):
    model = Addresses
    form_class = AddressForm
    success_url = reverse_lazy("account:address-list")
    template_name = "address/update.html"

    # check is owner or no


class AddressDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # security problem: csrf token

        try:
            address = Addresses.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404()

        if address.user != request.user:
            raise Http404()

        address.delete()
        messages.success(request, "address deleted.")
        return redirect(reverse("account:address-list"))


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Addresses
    form_class = AddressForm
    template_name = "address/create.html"
    success_url = reverse_lazy("account:address-list")

    def get_initial(self):
        return {
            "phone_number": self.request.user.phone_number,
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)
