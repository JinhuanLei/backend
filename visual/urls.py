from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testFunc/', views.testFunc, name='index'),
    path('testDB/', views.testDB, name='index'),
    path('createModel/', views.createModel, name='index'),
    path('models/', views.getModels, name='index'),

]
