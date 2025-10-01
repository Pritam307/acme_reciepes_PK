import graphene
from graphene import Field, Int, String, List
from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from graphql import GraphQLError
from django.shortcuts import get_object_or_404

class IngredientType(graphene.ObjectType):
    id = Int()
    name = String()
    description = String()

class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = String(required=True)
        description = String(required=False)

    ingredient = Field(lambda: IngredientType)

    def mutate(self, info, name, description=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")

        serializer = IngredientSerializer(data={"name": name, "description": description})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return CreateIngredient(ingredient=instance)

class UpdateIngredient(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        description = String()

    ingredient = Field(IngredientType)

    def mutate(self, info, id, name=None, description=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        obj = get_object_or_404(Ingredient, id=id)
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        serializer = IngredientSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return UpdateIngredient(ingredient=instance)

class DeleteIngredient(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
    ok = graphene.Boolean()

    def mutate(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        obj = get_object_or_404(Ingredient, id=id)
        obj.delete()
        return DeleteIngredient(ok=True)

class CreateRecipePayload(graphene.ObjectType):
    id = Int()
    title = String()
    description = String()
    ingredient_ids = List(Int)

class CreateRecipe(graphene.Mutation):
    class Arguments:
        title = String(required=True)
        description = String()
        ingredient_ids = List(Int)  # connect existing ingredients by id

    recipe = Field(lambda: graphene.JSONString)

    def mutate(self, info, title, description=None, ingredient_ids=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        # validate input with serializer
        serializer = RecipeSerializer(data={
            "title": title,
            "description": description or "",
            "ingredient_ids": ingredient_ids or []
        })
        serializer.is_valid(raise_exception=True)
        # create recipe
        recipe = Recipe.objects.create(title=serializer.validated_data["title"],
                                       description=serializer.validated_data.get("description", ""))
        # attach ingredients
        ids = serializer.validated_data.get("ingredient_ids", [])
        if ids:
            ingredients = Ingredient.objects.filter(id__in=ids)
            recipe.ingredients.set(ingredients)
        recipe.save()
        # return JSON-style data
        return CreateRecipe(recipe={
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "ingredient_ids": [i.id for i in recipe.ingredients.all()]
        })

class AddIngredientToRecipe(graphene.Mutation):
    class Arguments:
        recipe_id = Int(required=True)
        ingredient_id = Int(required=True)
    ok = graphene.Boolean()

    def mutate(self, info, recipe_id, ingredient_id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        recipe.ingredients.add(ingredient)
        return AddIngredientToRecipe(ok=True)

class RemoveIngredientFromRecipe(graphene.Mutation):
    class Arguments:
        recipe_id = Int(required=True)
        ingredient_id = Int(required=True)
    ok = graphene.Boolean()

    def mutate(self, info, recipe_id, ingredient_id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        recipe.ingredients.remove(ingredient)
        return RemoveIngredientFromRecipe(ok=True)
