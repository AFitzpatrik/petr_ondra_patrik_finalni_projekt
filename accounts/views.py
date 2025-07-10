from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.messages import success

from accounts.forms import SignUpForm


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
        #return redirect(request.META.get('HTTP_REFERER', '/'))  #zůstat na stejné stránce


class SignUpView(CreateView):
    template_name = 'registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        success(self.request, f'Účet pro uživatele {form.instance.username} byl úspěšně vytvořen!')
        return response
