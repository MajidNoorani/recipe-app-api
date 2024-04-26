"""
Views for the recipe API.
"""

from recipe import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework import (
    permissions,
    viewsets,
    mixins,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Recipe, Tag, Ingredient

"""
ModelViewSet:
provides a default implementation of CRUD operations for a Django model
It combines the functionality of GenericAPIView,
ListModelMixin, CreateModelMixin, RetrieveModelMixin,
UpdateModelMixin, and DestroyModelMixin

GenericViewSet is a generic class that does not provide any default actions
like ModelViewSet. By combining UpdateModelMixin, ListModelMixin,
and GenericViewSet, you are explicitly defining the behavior for
listing and updating models.
"""


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve recipe for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    # order of inputs is important
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    # order of inputs is important
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
