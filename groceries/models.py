from django.db import models
from django.contrib.auth.models import User

from recipes.models import Ingredient


class GroceryList(models.Model):
    owner = models.ForeignKey(User)
    ingredients = models.ManyToManyField(Ingredient)
    primary = models.BooleanField(default=True)

    def __str__(self):
        return "%s-%s" % (self.owner, self.primary)
