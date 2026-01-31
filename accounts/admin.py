from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ["email", "username", "first_name", "last_name", "is_staff"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {
            "fields": (
                "bio", "profile_image"
            ),
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            "fields": (
                "bio", "profile_image"
            ),
        }),
    )

admin.site.register(User, UserAdmin)
