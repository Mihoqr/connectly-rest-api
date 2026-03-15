from django.urls import path
from .views import UserListCreate, PostListCreate, PostDetailView, CommentListCreate, LikePostView, FeedView
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [

    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('login/', obtain_auth_token, name='login'),
    path('feed/', FeedView.as_view(), name='news-feed'),

    # SPECIFIC ROUTES
    path('<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('<int:pk>/comment/', CommentListCreate.as_view(), name='post-comment'),
    path('<int:pk>/comments/', CommentListCreate.as_view(), name='post-comments'),

    # DETAIL ROUTE
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # LIST / CREATE
    path('', PostListCreate.as_view(), name='post-list-create'),
]