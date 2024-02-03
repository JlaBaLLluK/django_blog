import random

from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from auth_user.models import AuthUser
from authorization.forms import LoginForm, ResetPasswordForm, SetNewPasswordForm
from registration.forms import VerificationForm


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


class ResetPasswordView(View):
    template_name = 'authorization/reset_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ResetPasswordForm})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        username_or_email = form.cleaned_data.get('username_or_email')
        if '@' in username_or_email:
            user = AuthUser.objects.get(email=username_or_email)
        else:
            user = AuthUser.objects.get(username=username_or_email)

        request.session['reset_password'] = True
        return redirect('email_verification', pk=user.pk)


class EmailVerificationView(View):
    template_name = 'authorization/email_verification.html'
    verification_code = None

    def get(self, request, pk):
        if 'reset_password' not in request.session:
            raise Http404()

        EmailVerificationView.verification_code = str(random.randint(100000, 999999))
        subject = 'Email Verification'
        message = (f"Your verification code is {EmailVerificationView.verification_code}. "
                   f"Enter this code to reset your password.")
        recipient_list = [AuthUser.objects.get(pk=pk).email]
        send_mail(subject, message, None, recipient_list)
        return render(request, self.template_name, {'form': VerificationForm})

    def post(self, request, pk):
        form = VerificationForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        user_code = ''.join(form.cleaned_data.values())
        if user_code != EmailVerificationView.verification_code:
            return render(request, self.template_name, {'form': form, 'error': 'This code is invalid!'}, status=400)

        del request.session['reset_password']
        request.session['set_new_password'] = True
        return redirect('set_new_password', pk)


class SetNewPasswordView(View):
    template_name = 'authorization/set_new_password.html'

    def get(self, request, pk):
        if 'set_new_password' not in request.session:
            raise Http404

        return render(request, self.template_name, {'form': SetNewPasswordForm})

    def post(self, request, pk):
        form = SetNewPasswordForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        user = AuthUser.objects.get(pk=pk)
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        del request.session['set_new_password']
        return redirect('login')


class LogoutView(View):
    @staticmethod
    def post(request):
        logout(request)
        return redirect('homepage')
