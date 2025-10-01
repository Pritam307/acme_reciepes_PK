from rest_framework import serializers
from .models import Recipe, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "description"]

class RecipeSerializer(serializers.ModelSerializer):
    ingredient_ids = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = Recipe
        fields = ["id", "title", "description", "ingredient_ids"]