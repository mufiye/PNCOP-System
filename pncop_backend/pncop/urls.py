from django.urls import path

from . import views

urlpatterns = [
    path('pncop/', views.compute_frequent_set)
]