from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from theatre.models import Play, Genre, Actor
from theatre.serializers import (
    PlayListSerializer,
    PlayDetailSerializer,
)

PLAY_URL = reverse("theatre:play-list")


def detail_url(play_id):
    return reverse("theatre:play-detail", args=(play_id,))


def sample_play(**params) -> Play:
    defaults = {"title": "Hamlet"}
    defaults.update(params)
    play = Play.objects.create(**defaults)
    genre = Genre.objects.create(name="Drama")
    actor = Actor.objects.create(first_name="Dave", last_name="Batista")

    play.genres.add(genre)
    play.actors.add(actor)
    return play


class UnauthenticatedPlayApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )

        self.client.force_authenticate(self.user)

    def test_play_list(self):
        sample_play()

        res = self.client.get(PLAY_URL)
        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_plays(self):
        play_1 = Play.objects.create(title="Hamlet")
        genre_drama = Genre.objects.create(name="Drama")
        actor_dave = Actor.objects.create(
            first_name="Dave", last_name="Batista"
        )

        play_1.genres.add(genre_drama)
        play_1.actors.add(actor_dave)

        play_2 = Play.objects.create(title="Kaidasheva simya")
        genre_comedy = Genre.objects.create(name="comedy")
        actor_ivan = Actor.objects.create(
            first_name="Ivan", last_name="Sirko"
        )

        play_2.genres.add(genre_comedy)
        play_2.actors.add(actor_ivan)

        res = self.client.get(
            PLAY_URL,
            {
                "genre": f"{genre_drama.id}, {genre_comedy.id}",
                "actor": f"{actor_dave.id}, {actor_ivan.id}",
            },
        )

        serializer_movie_1 = PlayListSerializer(play_1)
        serializer_movie_2 = PlayListSerializer(play_2)

        self.assertIn(serializer_movie_1.data, res.data)
        self.assertIn(serializer_movie_2.data, res.data)

    def test_retrieve_play_detail(self):
        play = sample_play()

        url = detail_url(play.id)
        res = self.client.get(url)
        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_forbidden(self):
        payload = {"title": "Gaidamaku"}

        res = self.client.post(PLAY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test",
            password="testpassword",
            is_staff=True,
        )

        self.client.force_authenticate(self.user)

    def test_create_play(self):
        genre = Genre.objects.create(name="Drama")
        actor = Actor.objects.create(first_name="Dave", last_name="Batista")
        payload = {
            "title": "Gaidamaku",
            "description": "A trilling play",
            "actors": [actor.id],
            "genres": [genre.id]
        }

        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            if key in ["actors", "genres"]:
                self.assertEqual(list(payload[key]), list(getattr(play, key).values_list('id', flat=True)))
            else:
                self.assertEqual(payload[key], getattr(play, key))

    def test_delete_play_not_allowed(self):
        play = sample_play()
        url = detail_url(play.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
