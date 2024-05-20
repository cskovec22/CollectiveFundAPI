from rest_framework.response import Response
from rest_framework import permissions, status, viewsets

from funds_collection.models import Collect, Payment
from .permissions import IsOwnerOrReadOnly
from .serializers import (CreatePaymentSerializer, PaymentSerializer, CreateCollectSerializer, CollectSerializer)
# from django.views.decorators.cache import cache_page
# from django.core.cache import cache
# from django.utils import timezone


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет для денежного сбора."""
    # queryset = cache.get_or_404(
        # f"collect_cache",
        # Collect.objects.all(),
        # timeout=60 * 10
    # )
    queryset = Collect.objects.all()
    http_method_names = ("get", "post", "patch", "delete")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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

    # @cache_page(60 * 10)
    # def list(self, request, *args, **kwargs):
    #     """Обеспечить кэширование данных на 10 минут."""
    #     return super().list(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет для платежа."""
    queryset = Payment.objects.all()
    http_method_names = ("get", "post")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        """Получить класс сериализатора."""
        if self.request.method in permissions.SAFE_METHODS:
            return PaymentSerializer
        return CreatePaymentSerializer

    def perform_create(self, serializer):
        """Обновить денежный сбор при создании платежа."""
        payment = serializer.save()

        fund = payment.collect
        fund.current_sum += payment.donation_sum
        fund.people_amount += 1
        fund.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

