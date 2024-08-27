from django.contrib import admin

from .models import CURRENT_COLUMNS, GOAL_COLUMNS, DailyIntakeTracking


class DailyIntakeTrackingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "date", *CURRENT_COLUMNS, *GOAL_COLUMNS)


admin.site.register(DailyIntakeTracking, DailyIntakeTrackingAdmin)
