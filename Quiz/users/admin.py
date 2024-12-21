from django.contrib import admin
from . models import User, Category, Teacher

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display= ('id','name', 'email', 'role', 'income')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display= ('id', 'name', 'description', 'created_by')

admin.site.register(User,UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Teacher)