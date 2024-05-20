from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    first_name = models.CharField("Имя", max_length=150, blank=True)
    patronymic = models.CharField("Отчество", max_length=150, blank=True)

    class Meta:
        """Конфигурация модели пользователя."""
        ordering = ("id",)
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return self.username

    def get_full_name(self):
        """Получить ФИО пользователя."""
        full_name = f"{self.last_name} {self.first_name} {self.patronymic}"
        return full_name.strip()
