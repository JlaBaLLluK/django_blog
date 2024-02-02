from django.urls import path

from registration.views import RegistrationView, RegistrationVerificationView, RegistrationSuccessView

urlpatterns = [
    path('', RegistrationView.as_view(), name='registration'),
    path('<int:pk>/registration-confirm/', RegistrationVerificationView.as_view(), name='registration_confirm'),
    path('registration-successful/', RegistrationSuccessView.as_view(), name='registration-successful')
]
