from django.urls import path

from . import views

app_name = 'web_collectors'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.create_collection, name='new_collection'),
    path('group/<slug:slug>/', views.collection_group, name='group'),
    path('group/<slug:slug>/<str:collection_name>', views.collection, name='collection'),
    path('group/<slug:slug>/<str:collection_name>/edit', views.update_collection, name='update_collection'),
    path('group/<slug:slug>/<str:collection_name>/new', views.create_item, name='new_item'),
    path('group/<slug:slug>/<str:collection_name>/<str:item_name>', views.collection_item, name='item'),
    path('group/<slug:slug>/<str:collection_name>/<str:item_name>/update', views.update_item, name='update_item'),
    path('groups/', views.collection_groups, name='groups'),

]
