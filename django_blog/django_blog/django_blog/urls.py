from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='homepage'),
    path('registration/', include('registration.urls')),
    path('authorization/', include('authorization.urls')),
    path('profile/', include('user_profile.urls'))
]
