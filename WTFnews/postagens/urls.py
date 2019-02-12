from django.urls import path

from postagens.views import CustomAuthToken
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('add/', views.AddPostView.as_view(), name='add_post'),
    path('api-token-auth/', obtain_auth_token),
    path('api-token-auth2/', CustomAuthToken.as_view()),
    path('delete/<int:post_id>', views.delete_post, name='delete_post'),
    path('share/<int:post_id>', views.SharePostView.as_view(), name='share'),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('posts', views.PostList.as_view(), name=views.PostList.name),
    path('posts/profiles', views.ProfileList.as_view(), name=views.ProfileList.name),
    path('posts/<int:pk>', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('posts/profiles/<int:pk>', views.ProfileDetail.as_view(), name=views.ProfileDetail.name),
]
