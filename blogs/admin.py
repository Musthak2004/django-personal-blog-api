from django.contrib import admin
from .models import Post, Comment, Like, Tag

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline, LikeInline]
    filter_horizontal = ("tags",)  # ✅ Only ManyToManyField

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
