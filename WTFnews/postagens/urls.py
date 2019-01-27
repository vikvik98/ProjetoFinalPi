from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.AddPostView.as_view(), name='add_post'),
    path('delete/<int:post_id>', views.delete_post, name='delete_post'),
]
