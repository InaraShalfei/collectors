from django.urls import path

from . import views

app_name = 'static_pages'

urlpatterns = [
    path('about/', views.AboutProjectView.as_view(), name='about'),
]
