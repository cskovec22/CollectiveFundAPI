from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from funds_collection.models import Collect, Payment
from .permissions import IsOwnerOrReadOnly
from .serializers import (CollectSerializer, CreateCollectSerializer,
                          CreatePaymentSerializer, PaymentSerializer)


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет для денежного сбора."""
    queryset = Collect.objects.select_related("author")
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
