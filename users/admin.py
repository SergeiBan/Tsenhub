from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Plan
from django.contrib.auth import get_user_model
from users.forms import CustomUserChangeForm, CustomUserCreationForm


User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('role', 'entity', 'email', 'plan', 'is_active')
    list_filter = ('plan',)

    fieldsets = (
        (None, {
            "fields": ('role', "email", "entity", "password", "plan")
        }),
        ('Статус', {
            'fields': ('is_active',)
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'role', "email", "entity", "password1", "password2", "plan"
                ),
        }),
        ('Статус', {
            'fields': ('is_active',)
        })
    )
    ordering = ['entity', '-date_joined']


class PlanAdmin(admin.ModelAdmin):
    list_display = ('discount', 'name')
    list_filter = ('discount',)


admin.site.register(Plan, PlanAdmin)
admin.site.register(User, CustomUserAdmin)
