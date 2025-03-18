from django.contrib import admin
from .models import Post
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'status')
    list_filter = ('status', 'created_date', 'published_date', 'author')
    search_fields = ('title', 'body', 'author')
    ordering = ['status', 'published_date']
    readonly_fields = ('slug',)
