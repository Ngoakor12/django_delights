from django import forms
from .models import Ingredient, MenuItem


class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "quantity", "unit", "unit_price"]


class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["title", "price", "image_url", "recipe_url"]
