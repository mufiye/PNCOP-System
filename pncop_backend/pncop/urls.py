from django.urls import path

from . import views

urlpatterns = [
    path('pncop/', views.compute_pncop_frequent_set),
    path('pacop/', views.compute_pacop_frequent_set)
]