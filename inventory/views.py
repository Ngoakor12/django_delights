from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import (
    IngredientCreateForm,
    MenuItemCreateForm,
    RecipeRequirementCreateForm,
    PurchaseCreateForm,
    IngredientUpdateForm,
)


# Create your views here.
class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredient_list.html"
    context_object_name = "ingredients"


class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase_list.html"
    context_object_name = "purchases"


@login_required
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


@login_required
def finances(request):
    context = {"revenue": 0, "cost": 0, "profit": 0}

    def get_purchase_prices(purchase):
        return purchase.menu_item.price

    purchases = Purchase.objects.all()
    purchase_prices = map(get_purchase_prices, purchases)
    revenue = sum(purchase_prices)
    context["revenue"] = round(revenue, 2)

    ingredients = Ingredient.objects.all()
    cost = 0
    for ingredient in ingredients:
        cost += ingredient.unit_price * ingredient.quantity
    context["cost"] = round(cost, 2)

    profit = revenue - cost
    context["profit"] = round(profit, 2)

    return render(request, "inventory/finances.html", context)


@login_required
def home_view(request):
    return redirect("inventory/menu_item/list")


@login_required
def ingredient_delete_all(request, pk):
    """delete all units of a given ingredient"""

    ingredients_match = Ingredient.objects.get(pk=pk)
    if ingredients_match:
        if ingredients_match.quantity != 0:
            ingredients_match.quantity = 0
            ingredients_match.save()

    return redirect(reverse("ingredient_list"))


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_create.html"
    form_class = IngredientCreateForm
    success_url = reverse_lazy("ingredient_list")


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_update.html"
    form_class = IngredientUpdateForm
    success_url = reverse_lazy("ingredient_list")


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory/menu_item_create.html"
    form_class = MenuItemCreateForm
    success_url = reverse_lazy("menu_item_list")


class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirement_create.html"
    form_class = RecipeRequirementCreateForm
    success_url = reverse_lazy("menu_item_list")


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "inventory/recipe_requirement_create.html"
    form_class = PurchaseCreateForm
    success_url = reverse_lazy("purchase_list")

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
        recipe_requirements_match = self.get_matching_recipe_requirements(
            form.instance.menu_item.pk
        )

        ingredients = Ingredient.objects.all()
        for recipe_requirement in recipe_requirements_match:
            for ingredient in ingredients:
                if recipe_requirement.ingredient.pk == ingredient.pk:
                    if recipe_requirement.quantity > ingredient.quantity:
                        return False
        return True

    def update_data(self, form):
        recipe_requirements_match = self.get_matching_recipe_requirements(
            form.instance.menu_item.pk
        )

        ingredients = Ingredient.objects.all()

        for recipe_requirement in recipe_requirements_match:
            for ingredient in ingredients:
                if recipe_requirement.ingredient.name == ingredient.name:
                    ingredient.quantity -= recipe_requirement.quantity
                    ingredient.save()

    def get_matching_recipe_requirements(self, menu_item_pk):
        recipe_requirements = RecipeRequirement.objects.all()

        def recipe_req_match(req):
            if req.menu_item.pk == menu_item_pk:
                return True
            return False

        return filter(recipe_req_match, recipe_requirements)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "registration/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
