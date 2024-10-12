from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
import random

from registration.forms import VerificationForm
from user_profile.forms import EditProfileDataForm, DeleteProfileForm


class UserProfileView(View):
    template_name = 'user_profile/user_profile.html'

    def get(self, request):
        return render(request, self.template_name)


class EditProfileDataView(View):
    template_name = 'user_profile/edit_profile_data.html'

    def get(self, request):
        form = EditProfileDataForm(initial={'username': request.user.username, 'email': request.user.email,
                                            'first_name': request.user.first_name, 'last_name': request.user.last_name})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        old_email = request.user.email
        form = EditProfileDataForm(request.POST, instance=request.user)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        new_email = form.cleaned_data.get('email')
        if old_email != new_email:
            user = form.save(commit=False)
            user.email = old_email
            user.save()
            request.session['new_email'] = new_email
            return redirect('email_update_verification')

        form.save()
        return redirect('user_profile')


class EmailUpdateVerificationView(View):
    template_name = 'user_profile/email_update_verification.html'
    verification_code = None

    def get(self, request):
        if 'new_email' not in request.session:
            raise Http404()

        EmailUpdateVerificationView.verification_code = str(random.randint(100000, 999999))
        subject = 'Email Verification'
        message = (f"Your verification code is {EmailUpdateVerificationView.verification_code}. "
                   f"Enter this code to  confirm  your new email.")
        recipient_list = [request.session['new_email']]
        send_mail(subject, message, None, recipient_list)
        return render(request, self.template_name, {'form': VerificationForm})

    def post(self, request):
        form = VerificationForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form}, status=400)

        user_code = ''.join(form.cleaned_data.values())
        if user_code != EmailUpdateVerificationView.verification_code:
            return render(request, self.template_name, {'form': form, 'error': 'This code is invalid!'}, status=400)

        request.user.email = request.session['new_email']
        request.user.save()
        del request.session['new_email']
        return redirect('user_profile')


class DeleteProfileView(View):
    template_name = 'user_profile/delete_profile.html'

    def get(self, request):
        return render(request, self.template_name, {'form': DeleteProfileForm})

    def post(self, request):
        form = DeleteProfileForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        request.user.delete()
        return redirect('homepage')
