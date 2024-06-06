from django.test import TestCase
from django.contrib.auth import get_user_model


class UserRegistrationTest(TestCase):

    def test_user_can_register_with_valid_email(self):
        email = "newemail@example.com"
        password = "password123"

        user = get_user_model().objects.create_user(email, password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)


class UserLoginTest(TestCase):

    def test_user_can_login_with_valid_credentials(self):
        email = "newemail@example.com"
        password = "password123"

        user = get_user_model().objects.create_user(email, password)
        user.is_active = True  # Activate the user
        user.save()

        logged_in = self.client.login(username=email, password=password)
        self.assertTrue(logged_in)

    def test_user_cannot_login_with_invalid_credentials(self):
        email = "newemail@example.com"
        invalid_passwords = ["wrongpassword", "12345"]

        for invalid_password in invalid_passwords:
            logged_in = self.client.login(
                username=email, password=invalid_password
            )
            self.assertFalse(logged_in)

            # Check for messages only if they exist
            messages = self.client.session.get("messages")
            if messages:
                self.assertIn(messages.ERROR, messages)
