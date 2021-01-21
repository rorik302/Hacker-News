from django.urls import path

from posts import views

urlpatterns = [
    path('', views.PostView.as_view())
]
