from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('visualization/', views.data_visualization, name='data-visualization'),
]