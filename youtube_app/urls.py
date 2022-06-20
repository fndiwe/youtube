from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('select/', views.select, name='select'),
    path('download/480', views.res480_version, name='res480'),
    path('download/720', views.res720_version, name='res720'),
    path('download/1080', views.res1080_version, name='res1080'),
    path("select-video/", views.select_video, name="select_video"),
    path("get-link/<str:video_id>/", views.get_link, name="get-link"),
    path("download/audio/", views.audio, name="audio"),
]
