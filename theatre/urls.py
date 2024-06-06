from django.urls import path, include
from rest_framework import routers
from theatre.views import (
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    ActorViewSet,
    GenreViewSet,
)

router = routers.DefaultRouter()

app_name = "theatre"
router.register("plays", PlayViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)

urlpatterns = [path("", include(router.urls))]
