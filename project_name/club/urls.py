from django.contrib import admin
from django.urls import path

from club.views import main_interface, location_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_interface, name='main_interface'),
    path('location_report/', location_report, name='location_report'),
]
