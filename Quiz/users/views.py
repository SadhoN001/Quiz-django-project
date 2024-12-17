from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Category, Teacher
from .serializers import (UserSerializer, UserCreateSerializer, CategorySerializer, TeacherSerializer,
                          UserRegisterSerializer, LoginSerializer)
from .permissions import IsTeacher
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

class UserView(ListCreateAPIView):
    """
    Handles listing all users and creating new ones.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


class UserProfile(RetrieveUpdateAPIView):
    """
    Handles retrieving and updating the authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user

class CategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get(self, request, *args, **kwargs):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_dashboard(self, request, *args, **kwargs):
        # Custom dashboard data
        return Response({'message': 'Teacher Dashboard Stats'})

    def get_students(self, request, *args, **kwargs):
        return Response({'students': []})

    def get_results(self, request, *args, **kwargs):
        return Response({'results': []})



class LoginView(APIView):
    permission_classes = [AllowAny]  # Ensure anyone can access this endpoint

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                "refresh": "your_refresh_token",
                "access": "your_access_token",
                "user": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "johndoe@example.com",
                    "role": "student",
                },
            },
            400: {"detail": "Invalid email or password."},
        },
    )
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate tokens manually
            refresh = RefreshToken()
            refresh['user_id'] = user.id

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "role": user.role,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Register(generics.CreateAPIView):
    serializer_class= UserRegisterSerializer
    permission_classes= []