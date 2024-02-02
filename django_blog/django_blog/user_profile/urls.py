from django.urls import path
from django.contrib.auth.decorators import login_required

from user_profile.views import UserProfileView, EditProfileDataView, EmailUpdateVerificationView

urlpatterns = [
    path('', login_required(UserProfileView.as_view()), name='user_profile'),
    path('edit-profile-data/', login_required(EditProfileDataView.as_view()), name='edit_profile_data'),
    path('edit-profile-data/email-update-confirm', login_required(EmailUpdateVerificationView.as_view()),
         name='email_update_verification')
]
