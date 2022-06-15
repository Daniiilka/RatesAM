from django.urls import path
from . import views

app_name = 'rates'
urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.show_results, name='result')
]