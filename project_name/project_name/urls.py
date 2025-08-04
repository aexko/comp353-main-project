from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('club/', include('club.urls')),
    re_path(r'^$', RedirectView.as_view(url='/club/', permanent=False)),
]
