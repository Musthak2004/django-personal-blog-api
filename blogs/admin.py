from django.contrib import admin
from .models import Post, Comment, Like

class LikeInline(admin.TabularInline):
    model = Like
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline, LikeInline]

admin.site.register(Post, PostAdmin)
