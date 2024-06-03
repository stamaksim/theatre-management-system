from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from theatre.models import Genre

GENRE_URL = reverse("theatre:genre-list")


def detail_genre_url(genre_id):
    return reverse("theatre:genre-detail", args=(genre_id,))


def sample_genre(**params) -> Genre:
    defaults = {
        "name": "Testgenre",
    }
    defaults.update(params)
    return Genre.objects.create(**defaults)


class UnauthenticatedGenreApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedGenreApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_genre(self):
        sample_genre()
        res = self.client.get(GENRE_URL)
        actors = Genre.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), actors.count())

    def test_create_genre_forbidden(self):
        payload = {"name": "comedy"}
        res = self.client.post(GENRE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminGenreApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test",
            password="testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_genre(self):
        payload = {"name": "comedy"}
        res = self.client.post(GENRE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        actor_id = res.data["id"]
        actor_from_response = Genre.objects.get(id=actor_id)

        for key in payload:
            self.assertEqual(payload[key], getattr(actor_from_response, key))

    def test_delete_actor_not_allowed(self):
        actor = sample_genre()
        url = detail_genre_url(actor.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
