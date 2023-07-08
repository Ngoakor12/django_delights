from django.db import models

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    unit_price = models.FloatField(default=0)


class MenuItem(models.Model):
    title = models.CharField(max_length=150)
    price = models.FloatField(default=0)
    image_url = models.CharField(default="", blank=True, null=True)
    recipe_url = models.CharField(default="", blank=True, null=True)


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    quantity = models.IntegerField(default=1)
