from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('gallery/<section_slug>/', views.showcase, name='showcase'),
    path('gallery/', views.section_list.as_view(), name='list_sections'),
    path('boards/', views.create_boards, name='create_boards'),
    path('sections/', views.create_sections, name='create_sections'),
    path('pins/', views.create_pins, name='create_pins'),
]