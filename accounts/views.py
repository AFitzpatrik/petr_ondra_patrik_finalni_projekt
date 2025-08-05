from django.contrib.auth import logout
from django.shortcuts import redirect

from django.views.generic import CreateView, View, TemplateView
from django.conf import settings

from accounts.forms import SignUpForm


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
