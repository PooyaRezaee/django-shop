from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_decode
from django.db import IntegrityError
from django.contrib import messages
from django.views.generic import ListView, UpdateView, CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .mixins import NoLoginMixin
from .forms import (
    LoginForm,
    RegisterForm,
    ProfileForm,
    AddressForm,
    ChangePasswordForm,
    RequestResetPasswordForm,
    SetPasswordForm,
)
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


class RequestResetPasswordView(View):
    template_name = "account/request_reset_password.html"
    form_class = RequestResetPasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                reset_url = user.get_password_reset_url()

                subject = "Password Reset Request"
                message = f"Your password reset request link: {reset_url}"

                send_mail(
                    subject,
                    message,
                    settings.FROM_EMAIL,
                    [email],
                )

            except User.DoesNotExist:
                pass

            messages.success(
                request,
                "If the email exists in our system, a password reset link will be sent.",
            )
            return redirect("main:home")

        messages.warning(request, "Form not valid.")
        return render(request, self.template_name, {"form": form})


class ResetPasswordView(View):
    template_name = "account/reset_password.html"
    form_class = SetPasswordForm
    token_generator = PasswordResetTokenGenerator()

    def get(self, request, uidb64=None, token=None):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and self.token_generator.check_token(user, token):
            form = self.form_class(initial={"token": token, "uidb64": uidb64})
            return render(request, self.template_name, {"form": form})
        else:
            messages.error(
                request, "The password reset link is invalid or has expired."
            )
            return redirect("home")

    def post(self, request, uidb64=None, token=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                uid = urlsafe_base64_decode(form.cleaned_data["uidb64"]).decode()
                user = User.objects.get(pk=uid)
                token = form.cleaned_data["token"]

                if user and self.token_generator.check_token(user, token):
                    user.set_password(form.cleaned_data["password1"])
                    user.save()
                    messages.success(
                        request, "Your password has been changed successfully."
                    )
                    return redirect("account:login")
                else:
                    messages.error(request, "Invalid reset link.")
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                messages.error(request, "An error occurred.")

        return render(request, self.template_name, {"form": form})


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
