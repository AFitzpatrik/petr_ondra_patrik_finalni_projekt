from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView
from django.contrib.messages import success

from accounts.forms import SignUpForm


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('logout_success')
        #return redirect(request.META.get('HTTP_REFERER', '/'))  #zůstat na stejné stránce


class SignUpView(CreateView):
    template_name = 'registration.html'
    form_class = SignUpForm

    def form_valid(self, form):
        self.object = form.save()
        success(self.request, f'Účet pro uživatele {form.instance.username} byl úspěšně vytvořen!')
        return redirect('registration_success')

class RegistrationSuccessView(TemplateView):
    template_name = 'registration_success.html'

class LogoutSuccessView(TemplateView):
    template_name = 'logout_success.html'
