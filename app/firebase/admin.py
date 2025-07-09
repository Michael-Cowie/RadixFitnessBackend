from django.contrib import admin

from .models import FirebaseUser


class FirebaseAdmin(admin.ModelAdmin):
    list_display = ("uid", "user")


admin.site.register(FirebaseUser, FirebaseAdmin)
