from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

def index_view(request):
    return render(request, 'index.html')

def makemigrations_view(request):
    return HttpResponse("Run `python manage.py makemigrations` in your terminal.")

def migrate_view(request):
    return HttpResponse("Run `python manage.py migrate` in your terminal.")

def createsuperuser_view(request):
    return HttpResponse("Run `python manage.py createsuperuser` in your terminal.")

def raw_sql_query_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM club_clubmember WHERE is_active = %s", [True])
        rows = cursor.fetchall()
    return render(request, 'raw_sql_query.html', {'rows': rows})

def query_view(request, query_number):
    queries = {
        '1': "SELECT * FROM club_clubmember WHERE first_name LIKE %s",
        '2': "SELECT * FROM club_clubmember WHERE last_name LIKE %s",
        '3': "SELECT * FROM club_clubmember WHERE date_of_birth < %s",
        '4': "SELECT * FROM club_clubmember WHERE social_security_number = %s",
        '5': "SELECT * FROM club_clubmember WHERE medicare_card_number = %s",
        '6': "SELECT * FROM club_clubmember WHERE telephone_number = %s",
        '7': "SELECT * FROM club_clubmember WHERE address LIKE %s",
        '8': "SELECT * FROM club_clubmember WHERE city = %s",
        '9': "SELECT * FROM club_clubmember WHERE province = %s",
        '10': "SELECT * FROM club_clubmember WHERE postal_code = %s",
        '11': "SELECT * FROM club_clubmember WHERE email_address = %s",
        '12': "SELECT * FROM club_location WHERE type = %s",
        '13': "SELECT * FROM club_location WHERE name LIKE %s",
        '14': "SELECT * FROM club_location WHERE address LIKE %s",
        '15': "SELECT * FROM club_location WHERE city = %s",
        '16': "SELECT * FROM club_location WHERE province = %s",
        '17': "SELECT * FROM club_location WHERE postal_code = %s",
        '18': "SELECT * FROM club_location WHERE phone_number = %s",
        '19': "SELECT * FROM club_location WHERE web_address LIKE %s",
        '20': "SELECT * FROM club_hobby WHERE name LIKE %s",
        '21': "SELECT * FROM club_log ORDER BY date DESC LIMIT 10"
    }

    query = queries.get(query_number, None)
    if not query:
        return HttpResponse("Invalid query number.")

    with connection.cursor() as cursor:
        cursor.execute(query, ['%test%'])  # Example parameter
        rows = cursor.fetchall()

    return render(request, 'query_results.html', {'rows': rows})
