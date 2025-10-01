from django.contrib import admin
from .models import Ingredient, Recipe
# Register your models here.

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "ingredient_count")