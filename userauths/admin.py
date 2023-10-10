from django.contrib import admin
from userauths.models import User, Profile


# Класс для отображения заданных колонок пользователя в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ["full_name", "username", "email", "gender"]


# Класс для отображения заданных колонок профлия пользователя в админке
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user", "verified"]
    list_editable = ["verified"]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
