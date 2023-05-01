from django.contrib import admin

from plans.models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('markup', 'name')
    list_filter = ('markup',)


admin.site.register(Plan, PlanAdmin)
