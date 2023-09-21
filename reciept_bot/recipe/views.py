from django.shortcuts import render
from recipe.models import Recipe


def serialize_recipe(recipe):
    return {
        "title": recipe.title,
        'cooking_time': recipe.cooking_time,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'price': recipe.price,
        'vegan_recipe': recipe.vegan_recipe,
        'category': recipe.category,
        'image': recipe.image
        # "slug": recipe.slug,
    }


def index(request):
    all_recipes = Recipe.objects.all()[:3]

    context = {
        'recipes': [serialize_recipe(recipe) for recipe in all_recipes]
    }
    return render(request, 'index.html', context)
