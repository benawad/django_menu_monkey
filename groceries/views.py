from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from recipes.models import Recipe, Ingredient
from .models import GroceryList


@login_required
def list_view(request):
    gl = get_object_or_404(GroceryList, owner=request.user, primary=True)

    return render(request, 'groceries/list.html', {'ingredients': gl.ingredients.all()})


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def add_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredient_set.all()
    try:
        gl = GroceryList.objects.get(owner=request.user, primary=True)
        gl.ingredients.add(*ingredients)
    except ObjectDoesNotExist:
        new_gl = GroceryList(owner=request.user, primary=True, )
        new_gl.save()
        new_gl.ingredients.add(*ingredients)

    return HttpResponseRedirect(reverse('index'))


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def ingredient_delete_view(request, ingredient_id):
    gl = get_object_or_404(GroceryList, owner=request.user, primary=True)
    gl.ingredients.remove(get_object_or_404(Ingredient, pk=ingredient_id))
    return HttpResponseRedirect(reverse('index'))
