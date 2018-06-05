from django.urls import path

from . import views

app_name = 'nbo'

urlpatterns = [
    # ex: /nbo/
    path('', views.index, name='index'),
    # # ex: /nbo/result/
    path('result/', views.result, name='result'),
]
