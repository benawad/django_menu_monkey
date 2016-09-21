from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.createRecipe, name='create'),
    url(r'^delete/(?P<recipe_id>[0-9]+)/$', views.delete_view, name='delete'),
    url(r'^show/(?P<recipe_id>[0-9]+)/$', views.show_view, name='show'),
    url(r'^search/recipe/$', views.search_recipe_view, name='search_recipe'),
]
