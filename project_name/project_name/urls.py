from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('club/', include('club.urls')),
    path('queries/', include('queries_asked.urls')),
]
