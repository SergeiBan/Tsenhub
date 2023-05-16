from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'role', 'entity', 'phone_number', 'email', 'plan', 'is_active')
    list_filter = ('plan',)

    fieldsets = (
        (None, {
            "fields": (
                'role', "email", 'phone_number', "entity", "password", "plan")
        }),
        ('Статус', {
            'fields': ('is_active',)
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'role', "email", 'phone_number', "entity", "password1",
                "password2", "plan"
            ),
        }),
        ('Статус', {
            'fields': ('is_active',)
        })
    )
    ordering = ['entity', '-date_joined']


admin.site.register(User, CustomUserAdmin)
