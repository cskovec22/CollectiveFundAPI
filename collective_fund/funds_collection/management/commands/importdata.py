import random

from django.core.management.base import BaseCommand

from funds_collection.models import Collect, Payment
from users.models import CustomUser


COUNT_COLLECTS = 2
COUNT_PAYMENTS = 10
COUNT_USERS = 4


class Command(BaseCommand):
    help = "Создает тестовые данные"

    def handle(self, *args, **options):
        self.create_users()
        self.create_collects()
        self.create_payments()

    def create_users(self):
        """Создание тестовых пользователей."""
        all_users = []

        for i in range(1, COUNT_USERS):
            password = f"User_{i}"
            user = CustomUser(
                username=f"User_{i}",
                email=f"user_{i}@user.ru",
                last_name="Фамилия",
                first_name="Имя",
                patronymic="Отчество"
            )
            user.set_password(password)
            all_users.append(user)

        CustomUser.objects.bulk_create(all_users)
        self.stdout.write(self.style.SUCCESS("Пользователи загружены"))
        return all_users

    def create_collects(self):
        """Создание тестовых сборов."""
        all_collects = []
        users = CustomUser.objects.all()

        for i in range(COUNT_COLLECTS):
            collect = Collect(
                author=random.choice(users),
                title=f"Название {i}",
                reason=random.choice(Collect.REASONS_CHOICES),
                description=f"Описание {i}",
                target_sum=random.randint(1000, 10000),
                image=f"data:image/png;base64,test_{i}",
                finish_date="2024-05-31T06:00:00Z"
            )

            all_collects.append(collect)

        Collect.objects.bulk_create(all_collects)
        self.stdout.write(self.style.SUCCESS("Групповые сборы загружены"))

    def create_payments(self):
        """Создание тестовых платежей."""
        all_payments = []
        users = CustomUser.objects.all()
        collects = Collect.objects.all()

        for i in range(COUNT_PAYMENTS):
            payment = Payment(
                author=random.choice(users),
                collect=random.choice(collects),
                donation_sum=random.randint(10, 100)
            )

            all_payments.append(payment)

        Payment.objects.bulk_create(all_payments)
        self.stdout.write(self.style.SUCCESS("Платежи загружены"))
