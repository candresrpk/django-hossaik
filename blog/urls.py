from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='post_create'),
    path('<slug:slug>/comment/', views.post_comment, name='post_comment'),


]
