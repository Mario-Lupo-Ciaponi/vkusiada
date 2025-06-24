from django.db import models


class CategoryChoices(models.TextChoices):
    STARTERS = "strs", "Starters"
    ENTREES = "ent", "Entrees"
    SALADS = "slds", "Salads"
    SOUPS = "sps", "Soups"
    MISCELLANEOUS = "mscl", "Miscellaneous"
    BEEF = "bf", "Beef"
    BREAKFAST = "brf", "Breakfast"
    DESSERT = "dsst", "Dessert"
    SEAFOOD = "sf", "Seafood"
    SIDE = "sd", "Side"
    CHICKEN = "ch", "Chicken"
    PORK = "prk", "Pork"
    PASTA = "ps", "Past"
    VEGETARIAN = "vgt", "Vegetarian"
    LAMB = "lmb", "Lamb"
    GOAT = "gt", "Goat"
