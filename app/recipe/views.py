"""
Views for the recipe API.
"""

from recipe import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework import (
    permissions,
    viewsets
)
from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Rtrieve recipe fpor authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
