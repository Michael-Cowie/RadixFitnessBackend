from django.contrib import admin

from .models import Firebase


class FirebaseAdmin(admin.ModelAdmin):
    list_display = ("uid", "user_id")


admin.site.register(Firebase, FirebaseAdmin)
