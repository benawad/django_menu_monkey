from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=9999)
    picture = models.ImageField(blank=True, null=True)
    instructions = models.TextField()
    owner = models.ForeignKey(User, related_name='owner')

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=9999)
    recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.name
