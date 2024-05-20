from django.contrib.admin import ModelAdmin, register

from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """Административный класс для модели пользователя."""
    list_display = ["username", "first_name"]
