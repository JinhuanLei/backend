from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testFunc/', views.testFunc, name='index'),
    path('testDB/', views.testDB, name='index'),
    path('createModel/', views.createModel, name='index'),
    path('models/', views.getModels, name='index'),
    path('quickstart/', views.quickStart, name='index'),
    path('model/<int:id>/', views.getModelById, name='index'),
    path('training/stop/<int:id>/', views.stopTraining, name='index'),
    path('training/<int:id>/', views.startTraining, name='index'),
    path('model/delete/<int:id>/', views.deleteModelById, name='index'),
]
