from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('gallery/<str:section_slug>/', views.pin_list.as_view(), name='showcase'),
    path('gallery/', views.section_list.as_view(), name='list sections'),
    path('boards/', views.create_boards, name='create boards'),
    path('sections/', views.create_sections, name='create sections'),
    path('pins/', views.create_pins, name='create pins'),
]