from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from theatre.models import Actor

ACTOR_URL = reverse("theatre:actor-list")


def detail_url(actor_id):
    return reverse("theatre:actor-detail", args=(actor_id,))


def sample_actor(**params) -> Actor:
    defaults = {
        "first_name": "Testname",
        "last_name": "Testlastname"
    }
    defaults.update(params)
    return Actor.objects.create(**defaults)


class UnauthenticatedActorApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ACTOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedActorApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_actors(self):
        sample_actor()
        res = self.client.get(ACTOR_URL)
        actors = Actor.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), actors.count())

    def test_create_actor_forbidden(self):
        payload = {"first_name": "John", "last_name": "Doe"}
        res = self.client.post(ACTOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminActorApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test",
            password="testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_actor(self):
        payload = {"first_name": "John", "last_name": "Dow"}
        res = self.client.post(ACTOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        actor_id = res.data["id"]
        actor_from_response = Actor.objects.get(id=actor_id)

        for key in payload:
            self.assertEqual(payload[key], getattr(actor_from_response, key))

    def test_delete_actor_not_allowed(self):
        actor = sample_actor()
        url = detail_url(actor.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
