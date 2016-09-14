from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from recipes.models import Recipe


@csrf_exempt
def list_view(request):
    if request.method == 'POST':
        recipe_ids = list(request.POST.values())
        recipes = Recipe.objects.filter(id__in=recipe_ids)
        ingredients = []
        for r in recipes:
            ingredients.extend(r.ingredient_set.all())

    return render(request, 'groceries/list.html', {'ingredients': ingredients})
