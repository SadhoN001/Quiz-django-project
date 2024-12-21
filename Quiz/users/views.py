from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Category, Teacher
from django.utils.functional import SimpleLazyObject
from .serializers import (UserSerializer, UserCreateSerializer, CategorySerializer, TeacherSerializer,
                          UserRegisterSerializer, LoginSerializer)
from .permissions import IsTeacher
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView


class UserView(ListAPIView):
    """
    Handles listing all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # Restrict allowed methods to GET only
    http_method_names = ['get']

@extend_schema(
    request=UserSerializer,
    responses=UserSerializer,
    description="Retrieve or update a user's profile by providing the ID in the request body."
)

class UserProfile(generics.UpdateAPIView):
    """
    Handles retrieving and updating a user's profile using the ID in the request body.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the user by ID from the request data
        user_id = self.request.data.get('id')  # Get ID from request body
        if not user_id:
            raise ValidationError({"id": "This field is required in the request body."})
        return get_object_or_404(User, id=user_id)

    
    
class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        # Check if 'created_by' is provided in the request
        created_by = serializer.validated_data.get('created_by', None)

        if not created_by:  # If not explicitly provided, use the authenticated user
            serializer.save(created_by=user)
        else:
            # Ensure the provided user is valid
            try:
                user_instance = User.objects.get(id=created_by.id)
                serializer.save(created_by=user_instance)
            except User.DoesNotExist:
                raise ValueError("The specified user does not exist.")


        

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


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