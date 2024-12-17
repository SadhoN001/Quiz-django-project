from rest_framework import serializers
from .models import User, Category, Teacher
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'income', 'active_field']
        read_only_fields = ['id']



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_role(self, value):
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role must be one of {valid_roles}.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Securely hash the password
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
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
    