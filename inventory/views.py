from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import (
    IngredientCreateForm,
    MenuItemCreateForm,
    RecipeRequirementCreateForm,
    PurchaseCreateForm,
)


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


def ingredient_delete(request, pk):
    """delete one unit of a given ingredient"""

    ingredients_match = Ingredient.objects.get(pk=pk)
    if ingredients_match:
        if ingredients_match.quantity != 0:
            ingredients_match.quantity -= 1
            ingredients_match.save()

    base_url = request.build_absolute_uri(reverse("ingredient_list"))
    return redirect(base_url)


def ingredient_delete_all(request, pk):
    """delete all units of a given ingredient"""

    ingredients_match = Ingredient.objects.get(pk=pk)
    if ingredients_match:
        if ingredients_match.quantity != 0:
            ingredients_match.quantity = 0
            ingredients_match.save()

    return redirect(reverse("ingredient_list"))


class IngredientCreateView(CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_create.html"
    form_class = IngredientCreateForm
    success_url = reverse_lazy("ingredient_list")


class MenuItemCreateView(CreateView):
    model = MenuItem
    template_name = "inventory/menu_item_create.html"
    form_class = MenuItemCreateForm
    success_url = reverse_lazy("menu_item_list")


class RecipeRequirementCreateView(CreateView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirement_create.html"
    form_class = RecipeRequirementCreateForm
    success_url = reverse_lazy("menu_item_list")


class PurchaseCreateView(CreateView):
    model = Purchase
    template_name = "inventory/recipe_requirement_create.html"
    form_class = PurchaseCreateForm
    success_url = reverse_lazy("menu_item_list")

    def form_valid(self, form):
        if not self.validate_data(form):
            # If the validation fails, display an error message and abort the save
            form.add_error(
                None,
                "The ingredients available are not enough to create that menu item",
            )
            return self.form_invalid(form)

        # Set the timestamp field before saving
        form.instance.timestamp = timezone.now()

        # update remaining ingredients
        self.update_data(form)

        # Save the form data
        return super().form_valid(form)

    def validate_data(self, form):
        recipe_requirements = RecipeRequirement.objects.filter(
            pk=form.instance.menu_item.pk
        )
        ingredients = Ingredient.objects.all()
        print(recipe_requirements)
        for recipe_requirement in recipe_requirements:
            for ingredient in ingredients:
                if recipe_requirement.ingredient.pk == ingredient.pk:
                    print("found match")
                    print(
                        f"{recipe_requirement.ingredient.name} - {recipe_requirement.quantity} - {ingredient.quantity}"
                    )
                    if recipe_requirement.quantity > ingredient.quantity:
                        print("not enough ingredients")
                        return False
        print("done validation")
        return True

    def update_data(self, form):
        recipe_requirements = RecipeRequirement.objects.filter(
            pk=form.instance.menu_item.pk
        )
        ingredients = Ingredient.objects.all()

        for recipe_requirement in recipe_requirements:
            for ingredient in ingredients:
                if recipe_requirement.ingredient.name == ingredient.name:
                    ingredient.quantity -= recipe_requirement.quantity
        print("done update")
        # ingredients.save()
