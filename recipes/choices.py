from django.db import models


class CategoryChoices(models.TextChoices):
    STARTERS = "Starters", "Starters"
    ENTREES = "Entrees", "Entrees"
    SALADS = "Salads", "Salads"
    SOUPS = "Soups", "Soups"
    MISCELLANEOUS = "Miscellaneous", "Miscellaneous"
    BEEF = "Beef", "Beef"
    BREAKFAST = "Breakfast", "Breakfast"
    DESSERT = "Dessert", "Dessert"
    SEAFOOD = "Seafood", "Seafood"
    SIDE = "Side", "Side"
    CHICKEN = "Chicken", "Chicken"
    PORK = "Pork", "Pork"
    PASTA = "Past", "Past"
    VEGETARIAN = "Vegetarian", "Vegetarian"
    LAMB = "Lamb", "Lamb"
    GOAT = "Goat", "Goat"
