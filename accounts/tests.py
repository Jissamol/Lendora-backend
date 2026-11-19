from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class SignupApiTests(APITestCase):
    def test_signup_creates_user_with_hashed_password(self):
        response = self.client.post(
            '/api/auth/signup/',
            {
                'name': 'Lendora Member',
                'email': 'member@example.com',
                'role': 'lender',
                'password': 'a-strong-password-123',
                'confirm_password': 'a-strong-password-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email='member@example.com')
        self.assertEqual(user.first_name, 'Lendora Member')
        self.assertEqual(user.role, get_user_model().Role.LENDER)
        self.assertTrue(user.check_password('a-strong-password-123'))

    def test_signup_rejects_duplicate_email_case_insensitively(self):
        get_user_model().objects.create_user(
            username='member@example.com',
            email='member@example.com',
            password='a-strong-password-123',
        )

        response = self.client.post(
            '/api/auth/signup/',
            {
                'name': 'Another Member',
                'email': 'MEMBER@example.com',
                'role': 'borrower',
                'password': 'a-strong-password-123',
                'confirm_password': 'a-strong-password-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_rejects_mismatched_password_confirmation(self):
        response = self.client.post(
            '/api/auth/signup/',
            {
                'name': 'Lendora Member',
                'email': 'member@example.com',
                'role': 'borrower',
                'password': 'a-strong-password-123',
                'confirm_password': 'a-different-password-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)

    def test_signup_rejects_admin_role(self):
        response = self.client.post(
            '/api/auth/signup/',
            {
                'name': 'New Admin',
                'email': 'admin@example.com',
                'role': 'admin',
                'password': 'a-strong-password-123',
                'confirm_password': 'a-strong-password-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_jwt_tokens_for_email_and_password(self):
        get_user_model().objects.create_user(
            username='member@example.com',
            email='member@example.com',
            password='a-strong-password-123',
        )

        response = self.client.post(
            '/api/auth/login/',
            {'username': 'member@example.com', 'password': 'a-strong-password-123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['role'], get_user_model().Role.BORROWER)

    def test_superuser_uses_django_admin_instead_of_frontend_login(self):
        user = get_user_model().objects.create_superuser(
            username='admin@example.com',
            email='admin@example.com',
            password='a-strong-password-123',
        )

        response = self.client.post(
            '/api/auth/login/',
            {'username': 'admin@example.com', 'password': 'a-strong-password-123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('admin portal', str(response.data).lower())
        self.assertTrue(self.client.login(username=user.username, password='a-strong-password-123'))

        admin_response = self.client.get('/admin/')

        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)