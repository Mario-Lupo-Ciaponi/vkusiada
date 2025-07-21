from django.contrib import admin

from accounts.models import VkusiadaUser, Profile


@admin.register(VkusiadaUser)
class VkusiadaUserAdmin(admin.ModelAdmin): ...


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): ...
