from django.contrib import admin
from plans.models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('discount', 'name')
    list_filter = ('discount',)


admin.site.register(Plan, PlanAdmin)
