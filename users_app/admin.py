from django.contrib import admin

from users_app.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'location', 'created_at']
    list_filter = ['type']
