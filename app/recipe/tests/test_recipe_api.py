"""
Tests for recipe APIs.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    """Create Recipe and return it."""
    defaults = {
        'title': 'Sample Recipe title',
        'time_minutes': 18,
        'price': Decimal('7.25'),
        'description': "Sample description of recipe.",
        'link': "http://example.com/recipe.pdf"
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test Unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Tests auth is required to call API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Test User',
            email='test@example.com',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Tests retrieving a list of recipes"""

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipes_limited_to_user(self):
        """Tests list of recipes is limited to authenticated user."""

        self.otheruser = get_user_model().objects.create_user(
            email='otheruser@example.com',
            password='testpassother'
        )
        create_recipe(self.user)
        create_recipe(self.otheruser)

        res = self.client.get(RECIPES_URL)

        recipes = get_user_model().objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
