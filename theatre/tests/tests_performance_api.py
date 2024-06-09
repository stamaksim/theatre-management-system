from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from theatre.models import Performance, Play, TheatreHall

PERFORMANCE_URL = reverse("theatre:performance-list")


def detail_url(performance_id):
    return reverse("theatre:performance-detail", args=(performance_id,))


def sample_play(title="Testplay"):
    return Play.objects.create(title=title)


def sample_theatre_hall(name="TestHall", rows=10, seats_in_row=10):
    return TheatreHall.objects.create(
        name=name, rows=rows, seats_in_row=seats_in_row
    )


def sample_performance(**params) -> Performance:
    defaults = {
        "play": sample_play(),
        "theatre_hall": sample_theatre_hall(),
        "show_time": "2024-06-03",
    }
    defaults.update(params)
    return Performance.objects.create(**defaults)


class UnauthenticatedPerformanceApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PERFORMANCE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPerformanceApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_performances(self):
        sample_performance()
        res = self.client.get(PERFORMANCE_URL)
        performances = Performance.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), performances.count())

    def test_create_performance_forbidden(self):
        payload = {
            "play": sample_play().id,
            "theatre_hall": sample_theatre_hall().id,
            "show_time": "2024-06-03",
        }
        res = self.client.post(PERFORMANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPerformanceApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test", password="testpassword", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_performance(self):
        play = sample_play()
        theatre_hall = sample_theatre_hall()
        payload = {
            "play": play.id,
            "theatre_hall": theatre_hall.id,
            "show_time": "2024-06-03",
        }
        res = self.client.post(PERFORMANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        performance = Performance.objects.get(id=res.data["id"])

        self.assertEqual(payload["play"], performance.play.id)
        self.assertEqual(payload["theatre_hall"], performance.theatre_hall.id)
        self.assertEqual(
            payload["show_time"], performance.show_time.strftime("%Y-%m-%d")
        )

    def test_delete_performance_not_allowed(self):
        performance = sample_performance()
        url = detail_url(performance.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filter_performance(self):
        play1 = sample_play(title="Ferdinand")
        play2 = sample_play(title="Kaidasheva simya")
        theatre_hall = sample_theatre_hall()

        performance_1 = sample_performance(
            play=play1, theatre_hall=theatre_hall, show_time="2024-06-01"
        )
        performance_2 = sample_performance(
            play=play2, theatre_hall=theatre_hall, show_time="2024-06-02"
        )

        res = self.client.get(
            PERFORMANCE_URL,
            {"date": "2024-06-01", "play": str(play1.id)},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], performance_1.id)
