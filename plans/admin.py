from django.contrib import admin

from plans.models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('multiplier', 'name')
    list_filter = ('multiplier',)


admin.site.register(Plan, PlanAdmin)
