from django.contrib import admin

from .models import Weights


class WeightsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'weight_kg', 'user_id')


admin.site.register(Weights, WeightsAdmin)
