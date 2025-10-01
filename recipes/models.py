from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def ingredient_count(self):
        # calculated field — NOT stored in DB
        return self.ingredients.count()

    def __str__(self):
        return self.title

