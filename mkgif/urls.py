from django.urls import path
from . import views


app_name = 'mkgif'

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:pk>/', views.details, name='details'),
    path('snippets/gif/<int:pk>/', views.gif, name='gif'),
    path('snippets/forms/images/', views.image_form, name='image_form'),
    path('snippets/forms/video/', views.video_form, name='video_form'),
]
