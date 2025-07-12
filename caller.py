import os
import django
from django.utils.text import slugify

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vkusiada.settings")
django.setup()

# Import your models
from accounts.models import VkusiadaUser
from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient

# Get the user
user = VkusiadaUser.objects.get(username="MarioLupo")

# Define soup recipes
soups = [
    {
        "name": "Classic Chicken Soup",
        "category": "Soups",
        "cuisine": "American",
        "youtube_link": "",
        "image_url": "https://example.com/chicken_soup.jpg",
        "instructions": "Boil chicken with vegetables and simmer until cooked. Add seasoning and serve hot.",
        "ingredients": [
            ("chicken", "200g"),
            ("carrot", "1 chopped"),
            ("celery", "1 stalk chopped"),
            ("onion", "1 chopped"),
            ("noodles", "1 cup"),
            ("salt", "to taste"),
            ("pepper", "to taste")
        ]
    },
    {
        "name": "Miso Soup",
        "category": "Soups",
        "cuisine": "Japanese",
        "youtube_link": "",
        "image_url": "https://example.com/miso_soup.jpg",
        "instructions": "Dissolve miso paste in dashi broth. Add tofu and wakame, then heat gently.",
        "ingredients": [
            ("miso paste", "2 tbsp"),
            ("dashi broth", "2 cups"),
            ("tofu", "100g cubed"),
            ("wakame", "1 tbsp"),
            ("green onion", "2 sliced")
        ]
    },
    {
        "name": "Tomato Basil Soup",
        "category": "Soups",
        "cuisine": "Italian",
        "youtube_link": "",
        "image_url": "https://example.com/tomato_basil.jpg",
        "instructions": "Simmer tomatoes with basil and garlic. Blend until smooth and serve warm.",
        "ingredients": [
            ("tomato", "4 chopped"),
            ("fresh basil", "A handful"),
            ("garlic", "2 cloves"),
            ("onion", "1 chopped"),
            ("olive oil", "1 tbsp"),
            ("salt", "to taste")
        ]
    },
    {
        "name": "Lentil Soup",
        "category": "Soups",
        "cuisine": "Middle Eastern",
        "youtube_link": "",
        "image_url": "https://example.com/lentil_soup.jpg",
        "instructions": "Cook lentils with spices, vegetables, and broth until soft. Blend or leave chunky.",
        "ingredients": [
            ("red lentils", "1 cup"),
            ("carrot", "1 diced"),
            ("celery", "1 stalk diced"),
            ("cumin", "1 tsp"),
            ("vegetable broth", "4 cups"),
            ("lemon juice", "1 tbsp")
        ]
    },
    {
        "name": "French Onion Soup",
        "category": "Soups",
        "cuisine": "French",
        "youtube_link": "",
        "image_url": "https://example.com/french_onion.jpg",
        "instructions": "Caramelize onions, deglaze with wine, and simmer in beef broth. Serve with cheesy toast.",
        "ingredients": [
            ("onion", "3 sliced"),
            ("butter", "2 tbsp"),
            ("beef broth", "4 cups"),
            ("dry white wine", "1/2 cup"),
            ("baguette", "sliced"),
            ("gruyère cheese", "100g grated")
        ]
    }
]

# Add each recipe
for soup in soups:
    recipe, created = Recipe.objects.get_or_create(
        name=soup["name"],
        defaults={
            "category": soup["category"],
            "cuisine": soup["cuisine"],
            "youtube_link": soup["youtube_link"],
            "image_url": soup["image_url"],
            "instructions": soup["instructions"],
            "author": user
        }
    )

    if created:
        for ing_name, measure in soup["ingredients"]:
            slug = slugify(ing_name.strip())
            ingredient, _ = Ingredient.objects.get_or_create(
                slug=slug,
                defaults={"name": ing_name.strip()}
            )

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                measure=measure
            )

        print(f"✔ Added '{recipe.name}'")
    else:
        print(f"⚠ '{recipe.name}' already exists")
