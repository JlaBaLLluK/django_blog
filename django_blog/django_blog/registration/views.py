from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
import random

from auth_user.models import AuthUser
from registration.forms import RegistrationForm, VerificationForm


class RegistrationView(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegistrationForm})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        form.save()
        request.session['allow_visit_confirmation_page'] = True
        return redirect('registration_verification', AuthUser.objects.get(username=form.cleaned_data.get('username')).pk)


class RegistrationVerificationView(View):
    template_name = 'registration/registration_verification.html'
    verification_code = None

    def get(self, request, pk):
        if 'allow_visit_confirmation_page' not in request.session:
            raise Http404()

        RegistrationVerificationView.verification_code = str(random.randint(100000, 999999))
        subject = "Confirm registration"
        message = (f"Your verification code is {RegistrationVerificationView.verification_code}. "
                   f"Enter this code to finish your registration.")
        recipient_list = [AuthUser.objects.get(pk=pk).email]
        send_mail(subject, message, None, recipient_list)
        return render(request, self.template_name, {'form': VerificationForm})

    def post(self, request, pk):
        form = VerificationForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        user_code = ''.join(form.cleaned_data.values())
        if user_code != RegistrationVerificationView.verification_code:
            return render(request, self.template_name, {'form': form, 'error': 'This code is invalid!'}, status=400)

        user = AuthUser.objects.get(pk=pk)
        user.is_active = True
        user.save()
        del request.session['allow_visit_confirmation_page']
        request.session['registration_success'] = True
        return redirect('registration_successful')


class RegistrationSuccessView(View):
    template_name = 'registration/registration_success.html'

    def get(self, request):
        if 'registration_success' not in request.session:
            raise Http404()

        del request.session['registration_success']
        return render(request, self.template_name)
