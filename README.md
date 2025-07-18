# Vkusiada

Vkusiada is an innovative, Django-based web platform designed to help users explore, share, 
and discover recipes with ease. Its goal is to answer the age-old question: “_What should I eat?_” 
by leveraging user input, ingredient tracking, and a vibrant recipe-sharing community.

---

## Table of Contents

- Features
- Demo
- Screenshots
- Getting Started
  - Prerequisites
  - Installation
  - Running Locally
- Usage
- Project Structure
- Contributing
- License
- Contact

---

## Features

- **Recipe Discovery**: Browse a curated library of recipes by category (Breakfast, Salads, Soups, etc.), cuisine, or ingredient.
- **Personalized Suggestions**: Add ingredients you have at home and get recipe suggestions tailored to your pantry.
- **Ingredient Library**: Build and manage your personal ingredient inventory.
- **Recipe Management**: Create, edit, and delete your own recipes with images, videos, and detailed instructions.
- **Favorites**: Save your favorite recipes for quick access.
- **User Profiles**: Each user gets a customizable profile with bio, location, cooking level, and activity history.
- **Community Features**:
  - Comment on recipes and share feedback.
  - Edit or delete your comments.
- **Media Support**: Recipes can include images and YouTube links for enhanced instructions.
- **Responsive Design**: Modern UI with category navigation, search, and mobile-friendly layouts.
- **Security**: Authentication and user management built on Django’s robust framework.

--- 

## Demo and screenshots

**Coming soon**

---

## Getting Started

### Prerequisites:

- Python 3.8 or higher
- Django 4.x
- (Recommended) Virtualenv for isolated Python environments

### Installation:

1. Clone the repository:

```shell
  git clone https://github.com/Mario-Lupo-Ciaponi/vkusiada.git
  cd vkusiada
```

2. Install the dependencies:

```shell
  pip install -r requirements.txt
```

3. Apply migrations:

```shell
  python manage.py migrate
```

4. (Optional) Create a superuser:

```shell
  python manage.py createsuperuser
```

5. Run the development server:

```shell
  python manage.py runserver
```

6. Visit http://127.0.0.1:8000/ in your browser.

---

## Usage

- **Browse Recipes**: Explore suggested and popular recipes on the homepage, filtered by your preferences or ingredients.
- **Search**: Use the search bar or category buttons to find recipes quickly.
- **Manage Profile**: Register or log in to save recipes, manage your ingredient library, and personalize your profile.
- **Interact**: Leave comments, share tips, and engage with other users in the community.
- **Create Recipes**: Share your own recipes with the community, including photos and video instructions.

---

## Project Structure

```
vkusiada/
│
├── accounts/            # User authentication and profile management
├── common/              # Shared utilities and components
├── ingredients/         # App for managing ingredients
├── recipes/             # Core app for recipe management
├── static/              # CSS files, images, and static assets
├── templates/           # Django HTML templates (accounts, recipes, common, etc.)
├── vkusiada/            # Main Django project settings and configuration
├── LICENSE              # MIT License
├── manage.py            # Django management script
├── README.md            # This file
└── requirements.txt     # Python dependencies
```
---

## Contributing

Contributions, bug reports, and feature requests are welcome!
To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a Pull Request explaining your changes.

---

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit).

---

## Contact

**Author**: Mario Lupo Ciaponi

**GitHub**: [Mario-Lupo-Ciaponi](https://github.com/Mario-Lupo-Ciaponi)

> Vkusiada is a labor of love—helping foodies and home cooks discover their next meal, one ingredient at a time.
