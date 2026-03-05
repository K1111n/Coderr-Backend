from django.contrib import admin

from reviews_app.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'business_user', 'rating', 'created_at']
    list_filter = ['rating']
