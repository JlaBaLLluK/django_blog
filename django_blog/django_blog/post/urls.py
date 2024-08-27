from django.contrib.auth.decorators import login_required
from django.urls import path

from post.views import WritePostView

urlpatterns = [
    path('write-post/', login_required(WritePostView.as_view()), name='write_post'),
]
