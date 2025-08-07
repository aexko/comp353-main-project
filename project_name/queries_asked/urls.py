# Python
from django.urls import path
from . import views

app_name = 'queries_asked'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('makemigrations/', views.makemigrations_view, name='makemigrations'),
    path('migrate/', views.migrate_view, name='migrate'),
    path('createsuperuser/', views.createsuperuser_view, name='createsuperuser'),
    path('raw-sql/', views.raw_sql_query_view, name='raw_sql_query'),
    path('query/<str:query_number>/', views.query_view, name='query'),
]
