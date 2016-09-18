from django.forms import ModelForm
from recipes.models import Recipe


class RecipeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['instructions'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = Recipe
        fields = ['title', 'picture', 'instructions']
