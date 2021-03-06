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
    path('playing/<int:id>/', views.validateModelById, name='index'),
    path('validating/<int:id>/', views.startValidating, name='index'),
    path('validating/stop/<int:id>/', views.stopValidating, name='index'),
    path('trainedModel/<int:id>/', views.updateTrainingPeriod, name='index')


]
