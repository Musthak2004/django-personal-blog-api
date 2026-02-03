from django import forms
from .models import Comment, Like, Tag

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write your comment...",
                "class": "w-full border rounded p-2"
            })
        }

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]