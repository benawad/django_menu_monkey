from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Recipe, Ingredient
from .forms import RecipeForm


def index(request):
    return render(request, 'recipes/list.html', {'recipes': get_list_or_404(Recipe), 'recipe_form': RecipeForm()})


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
    print(request.user)
    print(recipe.owner)
    if request.user == recipe.owner:
        recipe.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Unauthorized', status=401)
