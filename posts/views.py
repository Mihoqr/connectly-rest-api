from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


# Imports: Token Authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny 

# Imports
from .models import Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer

# --- DESIGN PATTERN IMPORTS ---
from singletons.logger_singleton import LoggerSingleton 

#For Integrating Third Party Services
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Initialize Singleton Logger
logger = LoggerSingleton().get_logger() 

# --- INTERNAL FACTORY CLASS ---
class PostFactory:
    @staticmethod
    def create_post(post_type, title, author, content='', metadata=None):
        # Sine-check nito kung valid ang post_type base sa choices sa models.py
        if post_type not in dict(Post.POST_TYPES):
            raise ValueError("Invalid post type")

        if post_type == 'image' and (not metadata or 'file_size' not in metadata):
            raise ValueError("Image posts require 'file_size' in metadata")
        
        if post_type == 'video' and (not metadata or 'duration' not in metadata):
            raise ValueError("Video posts require 'duration' in metadata")

        # Idinagdag ang author field para hindi mag-IntegrityError
        return Post.objects.create(
            title=title,
            author=author,
            content=content,
            post_type=post_type,
            metadata=metadata or {}
        )

# --- CUSTOM PERMISSION --- 
class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user

# --- USER LOGIC ---
@method_decorator(csrf_exempt, name='dispatch')  
class UserListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny] 

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            logger.info(f"User created: {user.username}")
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([]) 
@permission_classes([AllowAny])
@csrf_exempt
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    logger.info(f"Attempting login for: {username}")
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        logger.info(f"User login successful: {username}")
        return Response({
            "message": "Authentication successful!",
            "token": token.key,
            "username": user.username
        }, status=status.HTTP_200_OK) 
    
    logger.warning(f"Failed login attempt for user: {username}")
    return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED) 

# --- POST VIEWS WITH FACTORY PATTERN ---
@method_decorator(csrf_exempt, name='dispatch')
class PostListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        logger.info(f"Attempting to create a post: {data.get('title')}") 

        try:
            # I-pinasa natin ang request.user (ang logged-in user) sa Factory
            post = PostFactory.create_post(
                post_type=data.get('post_type'),
                title=data.get('title'),
                author=request.user, 
                content=data.get('content', ""),
                metadata=data.get('metadata', {})
            )
            
            logger.info(f"Post created successfully with ID: {post.id}") 
            return Response(
                {"message": "Post created successfully!", "post_id": post.id}, 
                status=status.HTTP_201_CREATED
            ) 

        except ValueError as e:
            logger.error(f"Post creation failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 

# --- UPDATED DETAIL VIEW --- 
class PostDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post)
        data = serializer.data

        # 🔥 Add these two lines
        data["like_count"] = Like.objects.filter(post=post).count()
        data["comment_count"] = Comment.objects.filter(post=post).count()

        return Response(data)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post is None:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, post)
        logger.info(f"Post ID {pk} deleted by user {request.user.username}")
        post.delete()
        return Response({"message": "Post deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

# --- UPDATED COMMENT VIEW ---@method_decorator(csrf_exempt, name='dispatch')
class CommentListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        comments = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        data = request.data.copy()
        data["post"] = pk
        data["author"] = request.user.id

        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(csrf_exempt, name='dispatch')
class LikePostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # pk = post id
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        # create like (prevent multiple likes because unique_together)
        try:
            Like.objects.create(user=request.user, post=post)
            return Response({"message": "Post liked!"}, status=status.HTTP_201_CREATED)
        except Exception:
            # most likely already liked
            return Response({"error": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
#------Google Login (Authentication)---------
class GoogleLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        google_id_token = request.data.get("id_token")

        if not google_id_token:
            return Response(
                {"error": "id_token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify token with Google
            idinfo = id_token.verify_oauth2_token(
                google_id_token,
                google_requests.Request()
            )

            email = idinfo.get("email")

            if not email:
                return Response(
                    {"error": "Email not found in token."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or get user
            user, created = User.objects.get_or_create(
                username=email.split("@")[0],
                defaults={"email": email}
            )

            # Create or get DRF token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            })

        except ValueError:
            return Response(
                {"error": "Invalid or expired Google token."},
                status=status.HTTP_401_UNAUTHORIZED
            )    

#------For News Feed API---------
class FeedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)  
