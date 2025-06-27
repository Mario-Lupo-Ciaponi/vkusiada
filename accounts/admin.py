from django.contrib import admin

from accounts.models import VkusiadaUser


@admin.register(VkusiadaUser)
class VkusiadaUserAdmin(admin.ModelAdmin):
    ...
