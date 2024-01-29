from django.urls import path

from registration.views import RegistrationView, RegistrationConfirmationView, RegistrationSuccessView

urlpatterns = [
    path('', RegistrationView.as_view(), name='registration'),
    path('<int:pk>/registration-confirm/', RegistrationConfirmationView.as_view(), name='registration_confirm'),
    path('registration-successful/', RegistrationSuccessView.as_view(), name='registration-successful')
]
