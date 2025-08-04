from django.shortcuts import render
from .models import Location

def main_interface(request):
    """
    Renders the main interface of the application.
    """
    return render(request, 'main_interface.html')

def location_report(request):
    """
    Handles the location report button click and displays the data.
    """
    locations = Location.objects.all().order_by('name')

    context = {
        'location_data': locations
    }
    return render(request, 'main_interface.html', context)
