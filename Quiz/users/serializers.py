from rest_framework import serializers
from .models import User, Category, Teacher
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)  # Make id editable and required for the request body

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'income', 'active_field']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )  # Allow selecting any user

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_by']
        read_only_fields = ['id']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Invalid email or password."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid email or password."})

        if not user.active_field:
            raise serializers.ValidationError({"detail": "Account is inactive."})

        data['user'] = user
        return data
        
class UserRegisterSerializer(serializers.Serializer):
    name= serializers.CharField(max_length= 100)
    password= serializers.CharField(write_only= True)
    email= serializers.EmailField()
         
    def validate_email(self, value):
        if User.objects.filter(email__iexact= value).exists():
             raise serializers.ValidationError("email already exits  !")
        return value
    
    def create(self, validated_data):
        user= User(
            name= validated_data["name"],
            email= validated_data['email'],
            password=make_password(validated_data["password"]) 
        )
        user.save()
        
        return User
    