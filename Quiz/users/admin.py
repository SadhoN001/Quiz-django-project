from django.contrib import admin
from . models import User, Category, Teacher

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display= ('name', 'email', 'role', 'income')

admin.site.register(User,UserAdmin)
admin.site.register(Category)
admin.site.register(Teacher)