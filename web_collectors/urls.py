from django.urls import path

from . import views

app_name = 'web_collectors'

urlpatterns = [
    path('', views.index, name='index'),
    path('delete_photo/<int:photo_id>', views.delete_photo, name='delete_photo'),
    path('groups/', views.collection_groups, name='groups'),
    path('all/', views.all_authors, name='all_authors'),
    path('new_collection/', views.create_collection, name='new_collection'),
    path('follow/', views.follow_index, name='follow_index'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('collection/<int:collection_id>/favorite', views.favorite_collection,
         name='favorite_collection'),
    path('collection/<str:username>/follow', views.profile_follow,
         name='profile_follow'),
    path('profile/<str:username>/unfollow', views.profile_unfollow,
         name='profile_unfollow'),
    path('profile/<str:username>/<int:collection_id>', views.author_collection,
         name='author_collection'),
    path('profile/<str:username>/<int:collection_id>/<int:item_id>',
         views.author_collection_item,
         name='author_collection_item'),
    path('group/<slug:slug>/', views.collection_group, name='group'),
    path('group/<slug:slug>/<int:collection_id>', views.collection,
         name='collection'),
    path('collection/<int:collection_id>/comment', views.add_comment,
         name='add_comment'),
    path('collection/<int:collection_id>/<int:comment_id>/reply',
         views.reply_comment, name='reply_comment'),
    path('collection/<int:collection_id>/<int:comment_id>/delete_comment',
         views.delete_comment,
         name='delete_comment'),
    path('collection/<int:collection_id>/<int:comment_id>/update_comment',
         views.update_comment,
         name='update_comment'),
    path('group/<slug:slug>/<int:collection_id>/edit', views.update_collection,
         name='update_collection'),
    path('collection/<int:collection_id>/delete', views.delete_collection,
         name='delete_collection'),
    path('group/<slug:slug>/<int:collection_id>/new', views.create_item,
         name='new_item'),
    path('group/<slug:slug>/<int:collection_id>/<int:item_id>',
         views.collection_item, name='item'),
    path('group/<slug:slug>/<int:collection_id>/<int:item_id>/update',
         views.update_item, name='update_item'),
    path('group/<slug:slug>/<int:collection_id>/<int:item_id>/delete',
         views.delete_item, name='delete_item'),

    ]
