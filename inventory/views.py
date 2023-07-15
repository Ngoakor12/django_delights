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


def menu_item_list(request):
    menu_items = MenuItem.objects.all()
    context = {"menu_items": []}
    for menu_item in menu_items:
        context["menu_items"].append(
            {
                "item": menu_item,
                "ingredients": menu_item.reciperequirement_set.all(),
            }
        )
        # for ingre in menu_item.reciperequirement_set.all():
        #     print(ingre.ingredient.name)

    return render(request, "inventory/menu_item_list.html", context)
