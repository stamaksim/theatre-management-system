from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
import user
from theatre.models import Reservation
from theatre.serializers import (
    ReservationListSerializer,
    ReservationDetailSerializer,
)

RESERVATION_URL = reverse("theatre:reservation-list")


def detail_url(reservation_id):
    return reverse("theatre:reservation-detail", args=(reservation_id,))


def sample_reservation(user=None, **params) -> Reservation:
    if user is None:
        user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
    defaults = {"user": user, "created_at": "03.06.2024"}
    defaults.update(params)
    return Reservation.objects.create(**defaults)


class UnauthenticatedPlayApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESERVATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReservationApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )

        self.client.force_authenticate(self.user)

    def test_reservation_list(self):
        sample_reservation(user=self.user)

        res = self.client.get(RESERVATION_URL)
        reservation = Reservation.objects.filter(user=self.user)
        serializer = ReservationListSerializer(reservation, many=True)
        response_data = res.data["results"]
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, serializer.data)

    def test_retrieve_reservation_detail(self):
        reservation = sample_reservation(user=self.user)

        url = detail_url(reservation.id)
        res = self.client.get(url)
        serializer = ReservationDetailSerializer(reservation)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_reservation(self):
        reservation = sample_reservation(user=self.user)
        url = detail_url(reservation.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_other_user_reservation(self):
        other_user = get_user_model().objects.create_user(
            email="other@test.test", password="testpassword"
        )
        reservation = sample_reservation(user=other_user)
        url = detail_url(reservation.id)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
