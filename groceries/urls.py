from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.list_view, name='list'),
    url(r'^add/(?P<recipe_id>[0-9]+)/$', views.add_view, name='add'),
    url(r'^remove/ingredient/(?P<ingredient_id>[0-9]+)/$', views.ingredient_delete_view, name='delete_ingredient'),
]
