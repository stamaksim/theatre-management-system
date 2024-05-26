from datetime import datetime
from django.db.models import F, Count
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
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
    ReservationSerializer,
    ActorSerializer,
    GenreSerializer,
    PlayListSerializer,
    PlayDetailSerializer, PerformanceListSerializer, PerformanceDetailSerializer, ReservationListSerializer
)


class PlayViewSet(
    ReadOnlyModelViewSet,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Play.objects.prefetch_related("actors", "genres")
    serializer_class = PlaySerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        elif self.action =="retrieve":
            return PlayDetailSerializer

        return PlaySerializer

    def get_queryset(self):
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actors__ids__in=actors_ids)

        return queryset.distinct()


class TheatreHallViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all().select_related(
        "play",
        "theatre_hall"
    ).annotate(
        tickets_available=(
            F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
            - Count("ticket")
        )
    ).order_by("id")
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        date = self.request.query_params.get("date")
        play_id_str = self.request.query_params.get("play")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if play_id_str:
            queryset = queryset.filter(play_id=int(play_id_str))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        elif self.action =="retrieve":
            return PerformanceDetailSerializer

        return PerformanceSerializer


class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play",
        "tickets__performance__theatre_hall"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



