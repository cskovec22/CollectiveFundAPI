from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from rest_framework import routers

from api.views import CollectViewSet, PaymentViewSet


router = routers.DefaultRouter()

router.register("collects", CollectViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("v1/", include(router.urls)),
]

urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    # path(
    #     "api/schema/redoc/",
    #     SpectacularRedocView.as_view(url_name="schema"),
    #     name="redoc"
    # ),
]
