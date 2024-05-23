import base64

from django.core.files.base import ContentFile
from django.core.mail import send_mail
from funds_collection.models import Collect, Payment
from rest_framework import serializers

from users.models import CustomUser


class Base64ImageField(serializers.ImageField):
    """Поле для декодирования изображения."""
    def to_internal_value(self, data):
        """Преобразовать изображение."""
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="image." + ext)

        return super().to_internal_value(data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для модели мользователя."""

    class Meta:
        """Конфигурация сериализатора для пользователя."""
        model = CustomUser
        fields = (
            "email",
            "username",
            "password",
            "last_name",
            "first_name",
            "patronymic"
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Создание пароля."""
        user = CustomUser(
            email=validated_data["email"],
            username=validated_data["username"],
            last_name=validated_data.get("last_name", ""),
            first_name=validated_data.get("first_name", ""),
            patronymic=validated_data.get("patronymic", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CreatePaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа."""

    class Meta:
        """Конфигурация сериализатора для создания платежа."""
        model = Payment
        fields = ["author", "collect", "donation_sum"]
        read_only_fields = ["author", "donation_date"]

    # def create(self, validated_data):
    #     """Вставить текущего пользователя в авторы платежа."""
    #     user = self.context["request"].user
    #     payment = Payment.objects.create(
    #         author=user,
    #         **validated_data
    #     )
    #
    #     send_mail(
    #         subject="Успешная отправка платежа",
    #         message=f"Ваш платеж {validated_data['donation_sum']} рублей "
    #                 "успешно отправлен на групповой сбор "
    #                 f"{validated_data['collect'].title}!",
    #         from_email="fundm@team.ru",
    #         recipient_list=[f"{user.email}"],
    #         fail_silently=True,
    #     )
    #
        # return payment

    def to_representation(self, instance):
        """Представление платежа."""
        serializer = PaymentSerializer(
            instance,
            context={"request": self.context.get("request")}
        )
        return serializer.data


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежа."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    collect = serializers.SlugRelatedField(
        slug_field="title",
        read_only=True
    )
    fio = serializers.SerializerMethodField()
    donation_date = serializers.SerializerMethodField()

    class Meta:
        """Конфигурация сериализатора для платежа."""
        model = Payment
        fields = [
            "author",
            "fio",
            "collect",
            "donation_sum",
            "donation_date"
        ]
        read_only_fields = ["author"]

    @staticmethod
    def get_fio(obj):
        """Получить ФИО автора платежа."""
        return obj.author.get_full_name()

    @staticmethod
    def get_donation_date(obj):
        donation_datetime = obj.donation_date
        formatted_datetime = donation_datetime.strftime("%d.%m.%Y в %H:%M")
        return formatted_datetime


class ListPaymentSerializer(PaymentSerializer):
    """Сериализатор для отображения списка платежей в денежном сборе."""

    class Meta:
        """Конфигурация сериализатора для списка платежей."""
        model = Payment
        fields = ["donation_sum", "donation_date", "fio"]


class CreateCollectSerializer(serializers.ModelSerializer):
    """Сериализатор для создания денежного сбора."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField()
    reason = serializers.ChoiceField(choices=Collect.REASONS_CHOICES)

    class Meta:
        """Конфигурация сериализатора для создания денежного сбора."""
        model = Collect
        fields = [
            "author",
            "title",
            "reason",
            "description",
            "target_sum",
            "image",
            "finish_date"
        ]
        read_only_fields = ["author"]

    # def create(self, validated_data):
    #     """Вставить текущего пользователя в авторы сбора."""
    #     user = self.context["request"].user
    #     collect = Collect.objects.create(
    #         author=user,
    #         **validated_data
    #     )
    #
    #     send_mail(
    #         subject="Успешное создание сбора",
    #         message=f"Ваш сбор {validated_data['title']} успешно создан!",
    #         from_email="fundm@team.ru",
    #         recipient_list=[f"{user.email}"],
    #         fail_silently=True,
    #     )
    #
        # return collect


class CollectSerializer(serializers.ModelSerializer):
    """Сериализатор для денежных сборов."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    current_sum = serializers.DecimalField(max_digits=8, decimal_places=2)
    people_amount = serializers.IntegerField()
    payment_list = serializers.SerializerMethodField()
    finish_date = serializers.SerializerMethodField()

    class Meta:
        """Конфигурация сериализатора для денежных сборов."""
        model = Collect
        fields = [
            "author",
            "title",
            "reason",
            "description",
            "target_sum",
            "current_sum",
            "people_amount",
            "image",
            "finish_date",
            "payment_list"
        ]
        read_only_fields = ["author"]

    @staticmethod
    def get_payment_list(collect):
        """Получить список пожертвований от других пользователей."""
        payments = collect.payments.all()
        serializer = ListPaymentSerializer(payments, many=True)
        return serializer.data

    @staticmethod
    def get_finish_date(obj):
        finish_datetime = obj.finish_date
        formatted_datetime = finish_datetime.strftime("%d %B %Y в %H:%M")
        return formatted_datetime
