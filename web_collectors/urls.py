from django.urls import path

from . import views

app_name = 'web_collectors'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.collection_group, name='group'),
    path('groups/', views.collection_groups, name='groups'),
]
