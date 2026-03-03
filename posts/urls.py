from django.urls import path
from .views import UserListCreate, PostListCreate, PostDetailView, CommentListCreate, LikePostView
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),

    # SPECIFIC ROUTES FIRST
    path('<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('<int:pk>/comment/', CommentListCreate.as_view(), name='post-comment'),
    path('<int:pk>/comments/', CommentListCreate.as_view(), name='post-comments'),

    # GENERIC ROUTE AFTER
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('', PostListCreate.as_view(), name='post-list-create'),

    path('login/', obtain_auth_token, name='login'),
]