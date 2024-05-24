from django.db.models import Sum, Count
from rest_framework import permissions, viewsets

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    CollectSerializer,
    CreateCollectSerializer,
    CreatePaymentSerializer,
    PaymentSerializer
)
from funds_collection.models import Collect, Payment


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет для денежного сбора."""
    queryset = Collect.objects.all()
    http_method_names = ("get", "post", "patch", "delete")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Получить queryset."""
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            "author"
        ).prefetch_related(
            "payments", "payments__author"
        ).annotate(
            people_amount=Count("payments__author", distinct=True),
            current_sum=Sum("payments__donation_sum", default=0)
        )
        return queryset

    def get_serializer_class(self):
        """Получить класс сериализатора."""
        if self.request.method in permissions.SAFE_METHODS:
            return CollectSerializer
        return CreateCollectSerializer

    def get_permissions(self):
        """Определить права доступа."""
        if self.request.method in ("PATCH", "DELETE"):
            return (IsOwnerOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Добавить автора перед созданием денежного сбора."""
        serializer.save(author=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет для платежа."""
    queryset = Payment.objects.all()
    http_method_names = ("get", "post")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Получить queryset."""
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            "author"
        ).prefetch_related("collect")
        return queryset

    def get_serializer_class(self):
        """Получить класс сериализатора."""
        if self.request.method in permissions.SAFE_METHODS:
            return PaymentSerializer
        return CreatePaymentSerializer

    def perform_create(self, serializer):
        """Обновить денежный сбор при создании платежа."""
        serializer.save(author=self.request.user)
