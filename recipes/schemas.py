import graphene
from graphene import ObjectType, Field, List, Int, String
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar
from django.core.paginator import Paginator

from .models import Ingredient, Recipe
from .mutations import (
    CreateIngredient, UpdateIngredient, DeleteIngredient,
    CreateRecipe, AddIngredientToRecipe, RemoveIngredientFromRecipe
)
from graphql import GraphQLError

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "description")

class RecipeType(DjangoObjectType):
    ingredient_count = Int()

    class Meta:
        model = Recipe
        fields = ("id", "title", "description", "ingredients", "ingredient_count")

    def resolve_ingredient_count(self, info):
        return self.ingredient_count()

class Query(ObjectType):
    # sanity check
    hello = graphene.String(description="A simple hello world field")
    # single recipe
    recipe = Field(RecipeType, id=Int(required=True))
    # list recipes (simple pagination)
    recipes = List(RecipeType, page=Int(default_value=1), page_size=Int(default_value=10))

    ingredient = Field(IngredientType, id=Int(required=True))
    ingredients = Field(GenericScalar, search=String(), page=Int(default_value=1), page_size=Int(default_value=10))


    # Require authenticated user at resolver-level:
    def resolve_recipe(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        return Recipe.objects.prefetch_related("ingredients").filter(id=id).first()

    def resolve_recipes(self, info, page, page_size):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        qs = Recipe.objects.all().order_by("-created_at")
        paginator = Paginator(qs, page_size)
        page_obj = paginator.get_page(page)
        return list(page_obj.object_list)

    def resolve_ingredient(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        return Ingredient.objects.filter(id=id).first()

    def resolve_ingredients(self, info, search=None, page=1, page_size=10):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        qs = Ingredient.objects.all().order_by("name")
        if search:
            qs = qs.filter(name__icontains=search)
        paginator = Paginator(qs, page_size)
        page_obj = paginator.get_page(page)
        # return as dict to include pagination meta
        return {
            "items": [ {"id": i.id, "name": i.name, "description": i.description} for i in page_obj.object_list ],
            "page": page,
            "page_size": page_size,
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }
    
    def resolve_hello(root, info):
        return "Hello World from GraphQL"

class Mutation(ObjectType):
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    delete_ingredient = DeleteIngredient.Field()

    create_recipe = CreateRecipe.Field()
    add_ingredient_to_recipe = AddIngredientToRecipe.Field()
    remove_ingredient_from_recipe = RemoveIngredientFromRecipe.Field()




schema = graphene.Schema(query=Query, mutation=Mutation)
