"""
URL configuration for django_delights project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    IngredientListView,
    PurchaseListView,
    menu_item_list,
    finances,
    home_view,
    IngredientUpdateView,
    ingredient_delete_all,
    IngredientCreateView,
    MenuItemCreateView,
    RecipeRequirementCreateView,
    PurchaseCreateView,
    login_view,
    logout_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path(
        "inventory/ingredient/list",
        IngredientListView.as_view(),
        name="ingredient_list",
    ),
    path(
        "inventory/ingredient/update/<int:pk>/",
        IngredientUpdateView.as_view(),
        name="ingredient_update",
    ),
    path(
        "inventory/ingredient/delete_all/<int:pk>/",
        ingredient_delete_all,
        name="ingredient_delete_all",
    ),
    path("inventory/purchase/list", PurchaseListView.as_view(), name="purchase_list"),
    path("inventory/menu_item/list", menu_item_list, name="menu_item_list"),
    path("finances", finances, name="finances"),
    path(
        "inventory/ingredient/create",
        IngredientCreateView.as_view(),
        name="ingredient_create",
    ),
    path(
        "inventory/menu_item/create",
        MenuItemCreateView.as_view(),
        name="menu_item_create",
    ),
    path(
        "inventory/recipe_requirement/create",
        RecipeRequirementCreateView.as_view(),
        name="recipe_requirement_create",
    ),
    path(
        "inventory/purchase/create",
        PurchaseCreateView.as_view(),
        name="purchase_create",
    ),
    path(
        "login",
        login_view,
        name="login",
    ),
    path(
        "logout",
        logout_view,
        name="logout",
    ),
]
