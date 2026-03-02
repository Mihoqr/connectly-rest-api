from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate 
from rest_framework.decorators import api_view
from rest_framework import generics

# Imports: Token Authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny 

# Imports
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

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
            serializer.save() 
            return Response({"message": "User created with hashed password!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({"message": "Authentication successful!"}, status=status.HTTP_200_OK) 
    return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED) 

# --- POST VIEWS WITH TOKEN AUTH & RBAC ---
@method_decorator(csrf_exempt, name='dispatch')
class PostListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- UPDATED DETAIL VIEW PARA SA DELETE TEST --- 
class PostDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)
        if post is None:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post is None:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, post)
        post.delete()
        return Response({"message": "Post deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

# Comment View
@method_decorator(csrf_exempt, name='dispatch')
class CommentListCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)