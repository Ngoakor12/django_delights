from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Ingredient, MenuItem, RecipeRequirement, Purchase


# Create your views here.
class IngredientListView(ListView):
    model = Ingredient
    template_name = "inventory/ingredient_list.html"
    context_object_name = "ingredients"


class PurchaseListView(ListView):
    model = Purchase
    template_name = "inventory/purchase_list.html"
    context_object_name = "purchases"
