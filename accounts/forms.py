from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "bio", "profile_image")

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "bio", "profile_image")