from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView

from django.views.generic import CreateView, View, TemplateView
from django.conf import settings

from accounts.forms import SignUpForm, CustomPasswordChangeForm


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
        # return redirect(request.META.get('HTTP_REFERER', '/'))#Nechat pro případ že chceme zůstat na stejné stránce


class LogoutSuccessView(TemplateView):
    template_name = "logout_success.html"


class SignUpView(CreateView):
    template_name = "registration.html"
    form_class = SignUpForm

    def form_valid(self, form):
        self.object = form.save()
        return redirect("registration_success")


class RegistrationSuccessView(TemplateView):
    template_name = "registration_success.html"


class LoginSuccessView(TemplateView):
    template_name = "login_success.html"


class PasswordChangeSuccessView(TemplateView):
    template_name = "password_change_success.html"


class CustomPasswordChangeView(DjangoPasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "password_change_form.html"
    
    def get_success_url(self):
        return reverse('password_change_success')
