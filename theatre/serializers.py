from rest_framework import serializers
from theatre.models import (
    Play,
    TheatreHall,
    Performance,
    Ticket,
    Reservation,
    Actor,
    Genre
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = (
            "first_name",
            "last_name",
            "full_name"
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres"
        )


class PlayListSerializer(PlaySerializer):
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="first_name"
    )
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )


class PlayDetailSerializer(PlaySerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres"
        )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "name",
            "rows",
            "capacity"
        )


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "show_time"
        )


class PerformanceListSerializer(PerformanceSerializer):
    performance_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity", read_only=True
    )
    ticket_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "performance_title",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "ticket_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "performance"

        )


class TicketSeatSerializer(TicketSerializer):
    class Meta:
        fields = ("row", "seat")


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(many=False, read_only=True)


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)
    taken_places = TicketSeatSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "play",
            "theatre_hall",
            "taken_places"
        )


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "tickets",
            "created_at",
        )


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
