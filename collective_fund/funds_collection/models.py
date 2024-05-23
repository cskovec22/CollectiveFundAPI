from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


MIN_COLLECTION_SUM = 1.0
MIN_DONATION_SUM = 1.0


class Payment(models.Model):
    """Модель платежа для сбора."""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        related_name="payments",
        verbose_name="Пользователь"
    )
    collect = models.ForeignKey(
        "Collect",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Денежный сбор"
    )
    donation_sum = models.DecimalField(
        "Сумма пожертвования",
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(MIN_DONATION_SUM)
        ]
    )
    donation_date = models.DateTimeField(
        "Дата пожертвования",
        auto_now_add=True
    )

    class Meta:
        """Конфигурация модели категории."""
        verbose_name = "платеж"
        verbose_name_plural = "Платежи"
        ordering = ("collect", "-donation_date")

    def __str__(self):
        """Строковое представление объекта категории."""
        return (f"{self.donation_date.strftime('%d %B %Y в %H:%M')} "
                f"пользователь {self.author} "
                f"пожертвовал {self.donation_sum} рублей")


class Collect(models.Model):
    """Модель группового денежного сбора."""
    REASONS_CHOICES = [
        ("birthday", "День рождения"),
        ("wedding", "Свадьба"),
        ("holiday", "Праздник"),
        ("child", "Рождение ребенка"),
        ("event", "Корпоративное мероприятие")
    ]

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="funds_collection",
        verbose_name="Автор группового денежного сбора"
    )
    title = models.CharField("Название", max_length=200)
    reason = models.CharField(
        "Причина",
        max_length=50,
        choices=REASONS_CHOICES
    )
    description = models.TextField("Описание")
    target_sum = models.DecimalField(
        "Сумма сбора",
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(MIN_COLLECTION_SUM)
        ],
        null=True,
        blank=True
    )
    image = models.ImageField(
        "Обложка сбора",
        upload_to="funds_collection/images/collect"
    )
    finish_date = models.DateTimeField("Дата завершения сбора")

    class Meta:
        """Конфигурация модели категории."""
        verbose_name = "сбор"
        verbose_name_plural = "Сборы"
        ordering = ("title",)

    def __str__(self):
        """Строковое представление объекта категории."""
        return self.title
