from django.db import models

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, blank=True)
    unit_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"


class MenuItem(models.Model):
    title = models.CharField(max_length=150)
    price = models.FloatField(default=0)
    image_url = models.CharField(max_length=300, default="", blank=True, null=True)
    recipe_url = models.CharField(max_length=300, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.title} - R{self.price}"


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} {self.ingredient.name} "


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.timestamp.time()} - {self.menu_item}"
