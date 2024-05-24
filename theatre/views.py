from rest_framework import mixins, viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from theatre.models import (
    Play,
    TheatreHall,
    Performance,
    Ticket,
    Reservation,
    Actor,
    Genre
)
from theatre.serializers import (
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    TicketSerializer,
    ReservationSerializer,
    ActorSerializer,
    GenreSerializer,
    PlayListSerializer,
    PlayDetailSerializer
)


class PlayViewSet(
    ReadOnlyModelViewSet,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Play.objects.prefetch_related("actors", "genres")
    serializer_class = PlaySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        elif self.action =="retrieve":
            return PlayDetailSerializer

        return PlaySerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.prefetch_related()

        return queryset


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



