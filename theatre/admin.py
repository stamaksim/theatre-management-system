from django.contrib import admin
from .models import (
    Play,
    TheatreHall,
    Performance,
    Ticket,
    Actor,
    Genre,
    Reservation,
)


admin.site.register(Play)
admin.site.register(TheatreHall)
admin.site.register(Performance)
admin.site.register(Ticket)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Reservation)
