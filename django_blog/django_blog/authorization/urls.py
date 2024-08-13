from django.contrib.auth.decorators import login_required
from django.urls import path

from authorization.views import LoginView, LogoutView, ResetPasswordView, EmailVerificationView, SetNewPasswordView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/<int:pk>/verify-email/', EmailVerificationView.as_view(), name='email_verification'),
    path('reset-password/<int:pk>/set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
    path('logout/', login_required(LogoutView.as_view()), name='logout')
]
