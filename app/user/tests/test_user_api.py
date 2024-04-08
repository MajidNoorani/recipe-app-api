"""Test for the user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """
    Test the public features of user API
    By public we mean that it they do not need
    authentication
    """
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test returning error for a user taht already exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test error is returned when password length is less than
        the pre-defined threshold
        """
        payload = {
            'email': 'test@example.com',
            'password': 'ps',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Tests generate token for valid credentials"""
        user_detail = {
            'name': "Test User",
            'email': 'test@exampl.com',
            'password': "test-pass-"
        }
        create_user(**user_detail)
        payload = {
            'email': user_detail['email'],
            'password': user_detail['password']
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_bad_credentials(self):
        """Test returns error if credentials invalid"""
        user_detail = {
            'name': "Test User",
            'email': 'test@exampl.com',
            'password': "correctpass"
        }
        create_user(**user_detail)
        payload = {
            'email': user_detail['email'],
            'password': 'wrongpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)