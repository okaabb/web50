from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/createPage", views.createPage, name="create"),
    path("wiki/new", views.new, name="new"),
    path("wiki/random", views.rand, name="random"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/save/<str:title>", views.save, name="save"),
    path("wiki/<str:title>", views.entry, name="entry"),   
]
