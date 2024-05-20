from django.apps import AppConfig
# from django.db.models.signals import post_save, post_delete


class FundsCollectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "funds_collection"
    verbose_name = "Сборы и платежи"

    # def ready(self):
    #     import FundsCollection.signals