from django.shortcuts import render, redirect
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

    return render(request, "inventory/menu_item_list.html", context)


def finances(request):
    context = {"revenue": 0, "cost": 0, "profit": 0}

    def get_purchase_prices(purchase):
        return purchase.menu_item.price

    purchases = Purchase.objects.all()
    purchase_prices = map(get_purchase_prices, purchases)
    revenue = sum(purchase_prices)
    context["revenue"] = round(revenue, 2)

    cost = 0
    for purchase in purchases:
        recipe_reqs = purchase.menu_item.reciperequirement_set.all()
        for recipe_req in recipe_reqs:
            cost += recipe_req.ingredient.unit_price * recipe_req.quantity
    context["cost"] = round(cost, 2)

    profit = revenue - cost
    context["profit"] = round(profit, 2)

    return render(request, "inventory/finances.html", context)


def home_view(request):
    return redirect("inventory/menu_item/list")
