from django.contrib import admin
from django.urls import path, include
from django.views.generic import ListView

from post.models import Post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ListView.as_view(template_name='index.html',
                              model=Post,
                              context_object_name='posts',
                              queryset=Post.objects.order_by('-pk').all()), name='homepage'),
    path('registration/', include('registration.urls')),
    path('authorization/', include('authorization.urls')),
    path('profile/', include('user_profile.urls')),
    path('posts/', include('post.urls')),
]
