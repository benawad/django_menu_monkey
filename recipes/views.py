from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Recipe, Ingredient
from .forms import RecipeForm
import json


def index(request):
    return render(request, 'recipes/list.html', {'recipes': Recipe.objects.all(), 'recipe_form': RecipeForm()})


def search_recipe_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        return render(request, 'recipes/search_recipe.html', {'recipes': Recipe.objects.filter(title__icontains=query)})


def search_ingredient_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', '[]')
        query = json.loads(query)
        if len(query) > 0:
            recipes = []
            for ing in query:
                i = Ingredient.objects.get(name=ing)
                recipes.extend(i.recipes.all())
        else:
            recipes = Recipe.objects.all()
        return render(request, 'recipes/search_ingredient.html', {'recipes': recipes, 'ingredients': Ingredient.objects.values('name').distinct()})


@login_required
def createRecipe(request):
    if request.method == 'GET':
        recipe_form = RecipeForm()
    elif request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            ingredients = request.POST['ingredients'].strip()
            if ingredients != "":
                for i in ingredients.split("\n"):
                    i = i.strip()
                    same_name = Ingredient.objects.filter(name__iexact=i)
                    if same_name.exists():
                        same_name[0].recipes.add(recipe)
                    else:
                        ing = Ingredient(name=i.strip())
                        ing.save()
                        ing.recipes.add(recipe)
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'recipes/create.html', {'recipe_form': recipe_form})


@require_http_methods(["POST"])
@login_required
@csrf_exempt
def delete_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user == recipe.owner:
        recipe.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Unauthorized', status=401)


def show_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/show.html', {'recipe': recipe, 'ingredients': recipe.ingredient_set.all()})
