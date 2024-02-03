from django.urls import path

from registration.views import RegistrationView, RegistrationVerificationView, RegistrationSuccessView

urlpatterns = [
    path('', RegistrationView.as_view(), name='registration'),
    path('<int:pk>/registration-verification/', RegistrationVerificationView.as_view(), name='registration_verification'),
    path('registration-successful/', RegistrationSuccessView.as_view(), name='registration_successful')
]
