from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class postInfoAdmin(admin.ModelAdmin):
    list_display = ["post_title", "post_body", "post_created"]
    search_fields = ["post_title", "post_body"]
    def has_add_permission(self, request):
        return False

class likesAdmin(admin.ModelAdmin):    
    def has_module_permission(self, request):
        return False
    
class repliesAdmin(admin.ModelAdmin):    
    def has_module_permission(self, request):
        return False

class reply_likesAdmin(admin.ModelAdmin):    
    def has_module_permission(self, request):
        return False
    
class ProfileAdmin(admin.ModelAdmin):    
    pass
    
class StudentUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets

admin.site.register(postInfo, postInfoAdmin)
admin.site.register(likes, likesAdmin) 
admin.site.register(replies, repliesAdmin)
admin.site.register(reply_likes, reply_likesAdmin)
admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(Profile, ProfileAdmin)
