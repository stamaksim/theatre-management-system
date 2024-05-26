from django.urls import path, include
from rest_framework import routers
from theatre.views import (
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    ActorViewSet,
    GenreViewSet
)

router = routers.DefaultRouter()

app_name = "theatre"
router.register("plays", PlayViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("performance", PerformanceViewSet)
router.register("reservation", ReservationViewSet)
router.register("actor", ActorViewSet)
router.register("genre", GenreViewSet)

urlpatterns = [path("", include(router.urls))]
