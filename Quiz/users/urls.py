from django.urls import path
from .views import(UserView, UserProfile, CategoryListView, 
                   CategoryDetailView, TeacherView, LoginView, Register)

urlpatterns = [
    # User endpoints
    path('users/', UserView.as_view(), name='user-list'),
    path('profile/', UserProfile.as_view(), name='user-profile'),
    
    # Category endpoints
   path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Teacher endpoints
    path('teachers/', TeacherView.as_view(), name='teacher-list'),
    path('teachers/dashboard/', TeacherView.as_view(), name='teacher-dashboard'),
    path('teachers/students/', TeacherView.as_view(), name='teacher-students'),
    path('teachers/results/', TeacherView.as_view(), name='teacher-results'),
    
    # Authentication
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/Register/', Register.as_view(), name='Register'),
]
