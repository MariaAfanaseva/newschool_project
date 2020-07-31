from django.contrib import admin
from authapp.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_display = ('email', 'name',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
