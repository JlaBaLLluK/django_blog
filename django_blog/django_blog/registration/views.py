from django.shortcuts import render
from django.views import View

from registration.forms import RegistrationForm


class RegistrationView(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegistrationForm})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': RegistrationForm})
