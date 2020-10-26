from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('result/', views.result, name='result'),
    #path('checkText/', views.check_text, name='check_text'),
    path('regenerate/', views.regenerate, name='regenerate'),
    path('download/', views.download, name='download'),
]
