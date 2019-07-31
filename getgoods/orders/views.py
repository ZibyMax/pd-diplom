from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView
from .forms import LoginForm, ForgotForm


def index(request):
    return render(request, 'index.html')


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'login.html'


class RegisterFormView(FormView):
    form_class = LoginForm
    template_name = 'register.html'


class ForgotFormView(FormView):
    form_class = ForgotForm
    template_name = 'forgot.html'

