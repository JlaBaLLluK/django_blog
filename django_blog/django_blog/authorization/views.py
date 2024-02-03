from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View

from auth_user.models import AuthUser
from authorization.forms import LoginForm


class LoginView(View):
    template_name = 'authorization/login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': LoginForm})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        username_or_email = form.cleaned_data.get('username_or_email')
        if '@' in username_or_email:
            user = AuthUser.objects.get(email=username_or_email)
        else:
            user = AuthUser.objects.get(username=username_or_email)

        if not user.is_active:
            request.session['allow_visit_confirmation_page'] = True
            return redirect('registration_verification', pk=user.pk)

        login(request, user)
        return redirect('user_profile')


class ForgoPasswordView(View):
    template_name = 'authorization/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


class LogoutView(View):
    @staticmethod
    def post(request):
        logout(request)
        return redirect('homepage')
