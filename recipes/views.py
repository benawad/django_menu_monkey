from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Recipe, Ingredient
from .forms import RecipeForm

from imgurpython import ImgurClient
import os


def index(request):
    return render(request, 'recipes/list.html', {'recipes': Recipe.objects.all(), 'recipe_form': RecipeForm()})


def search_recipe_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        return render(request, 'recipes/search_recipe.html', {'recipes': Recipe.objects.filter(title__icontains=query)})


def search_ingredient_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        ingredients = Ingredient.objects.filter(name__icontains=query)
        recipes = []
        for i in ingredients:
            recipes.extend(i.recipes.all())
        recipes = set(recipes)
        return render(request, 'recipes/search_ingredient.html', {'recipes': recipes})


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
            url = settings.BASE_DIR + recipe.picture.url
            recipe.imgur_url = (_upload_to_imgur(url)['link'])
            recipe.save()
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


def _upload_to_imgur(path):
    client_id = os.environ['IMGUR_CLIENT_ID']
    client_secret = os.environ['IMGUR_CLIENT_SECRET']

    client = ImgurClient(client_id, client_secret)
    url = client.upload_from_path(path)
    return url
