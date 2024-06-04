from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from theatre.models import TheatreHall

THEATRE_HALL_URL = reverse("theatre:theatrehall-list")


def detail_theatre_hall_url(theatre_hall_id):
    return reverse("theatre:theatrehall-detail", args=(theatre_hall_id,))


def sample_theatre_hall(**params) -> TheatreHall:
    defaults = {
        "name": "Oskar",
        "rows": 1,
        "seats_in_row": 1
    }
    defaults.update(params)
    return TheatreHall.objects.create(**defaults)


class UnauthenticatedTheatreHallApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(THEATRE_HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTheatreHallApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_theatre_hall(self):
        sample_theatre_hall()
        res = self.client.get(THEATRE_HALL_URL)
        theatre_halls = TheatreHall.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), theatre_halls.count())

    def test_create_theatre_hall_forbidden(self):
        payload = {"name": "Grand Hall", "rows": 5, "seats_in_row": 10}
        res = self.client.post(THEATRE_HALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTheatreHallApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test",
            password="testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_theatre_hall(self):
        payload = {"name": "Grand Hall", "rows": 5, "seats_in_row": 10}
        res = self.client.post(THEATRE_HALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        theatre_hall_id = res.data["id"]
        theatre_hall_from_response = TheatreHall.objects.get(id=theatre_hall_id)

        for key in payload:
            self.assertEqual(payload[key], getattr(theatre_hall_from_response, key))

    def test_delete_theatre_hall_not_allowed(self):
        theatre_hall = sample_theatre_hall()
        url = detail_theatre_hall_url(theatre_hall.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
