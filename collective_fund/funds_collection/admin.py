from django.contrib.admin import ModelAdmin, register, TabularInline

from .models import Collect, Payment


@register(Payment)
class PaymentAdmin(ModelAdmin):
    """Административный класс для модели платежа."""
    list_display = ["author", "donation_sum", "donation_date"]
    readonly_fields = ["author", "donation_date"]

# class PaymentsInline(TabularInline):
#     model = Payment


@register(Collect)
class CollectAdmin(ModelAdmin):
    """Административный класс для сбора."""
    list_display = [
        "id",
        "author",
        "title",
        "reason",
        "target_sum",
        "current_sum",
        "people_amount",
        "finish_date"
    ]
    readonly_fields = ["author", "current_sum", "people_amount"]
    # inlines = [PaymentsInline]

