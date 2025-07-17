from django.urls import path
from . import views
from .views import PostUpdate, PostDelete, GlobalFeedView

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),

    path('user_feed/', views.user_feed, name='user_feed'),
    path('profile.<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    path('posts/create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),   
    
    path('global_feed/', GlobalFeedView.as_view(), name='global_feed'),

    path('comments/reply/', views.reply_to_comment, name='reply_to_comment'),
]
