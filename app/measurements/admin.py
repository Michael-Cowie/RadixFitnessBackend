from django.contrib import admin

from .models import WeightEntry


class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "weight_kg", "user")


admin.site.register(WeightEntry, WeightEntryAdmin)
