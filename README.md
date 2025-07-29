# Vkusiada

Vkusiada is a Django-based web platform for recipe sharing and discovery. It helps users find new recipes, manage ingredients, and connect with a community of food lovers.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Recipe Discovery**: Browse recipes by category, cuisine, or ingredients.
- **Personalized Suggestions**: Get recipe recommendations based on the ingredients you have.
- **Ingredient Management**: Keep track of your pantry with a personal ingredient library.
- **Recipe Creation**: Share your own recipes with photos, videos, and detailed instructions.
- **User Profiles**: Customize your profile, track your activity, and connect with other users.
- **Community Engagement**: Comment on recipes, share feedback, and participate in a vibrant food community.
- **Responsive Design**: Enjoy a seamless experience across all devices.

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Styling**: CSS
- **Formatting**: Black

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mario-Lupo-Ciaponi/vkusiada.git
   cd vkusiada
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Change in setting DATABASES**:
   Change DATABASES variable in the project:
   ```python
   DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "vkusiada_db",
        "USER": "your username",
        "PASSWORD": "your password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
   ```

5. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- **Browse and search for recipes**: Explore the recipe library and use the search functionality to find specific dishes.
- **Manage your profile**: Register or log in to create a profile, save your favorite recipes, and manage your ingredient inventory.
- **Create and share recipes**: Share your culinary creations with the community by adding new recipes.
- **Engage with the community**: Comment on recipes, ask questions, and connect with other food enthusiasts.

## Project Structure

```
vkusiada/
├── accounts/         # User authentication and profile management
├── common/           # Shared utilities and components
├── ingredients/      # Ingredient management
├── recipes/          # Recipe creation and management
├── static/           # Static assets (CSS, images)
├── templates/        # HTML templates
├── vkusiada/         # Django project settings and configuration
├── .flake8           # Flake8 linter settings
├── .pre-commit-config.yaml # Pre-commit hook configurations
├── LICENSE           # MIT License
├── manage.py         # Django management script
├── pyproject.toml    # Black formatter settings
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit).

## Contact

**Author**: Mario Lupo Ciaponi
**GitHub**: [Mario-Lupo-Ciaponi](https://github.com/Mario-Lupo-Ciaponi)