# Vkusiada - Recipe Platform Documentation

## Overview

Vkusiada is an innovative, Django-based web platform designed to help users explore, share, and discover recipes with ease. The platform addresses the common question "What should I eat?" by leveraging user input, ingredient tracking, and fostering a vibrant recipe-sharing community.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

### Core Functionality
- **Recipe Discovery**: Browse extensive recipe collections organized by category, cuisine type, or available ingredients
- **Personalized Recipe Suggestions**: Intelligent recommendation system that suggests recipes based on your current ingredient inventory
- **Ingredient Management**: Personal pantry tracking system to monitor available ingredients and their quantities
- **Recipe Creation & Sharing**: Comprehensive recipe authoring tools with support for photos, videos, and detailed step-by-step instructions

### Community Features
- **User Profiles**: Customizable user profiles with activity tracking and social connectivity
- **Community Engagement**: Interactive comment system, recipe feedback, and community participation features
- **Social Connectivity**: Connect with fellow food enthusiasts and discover new culinary inspirations

### Technical Features
- **Responsive Design**: Optimized user experience across desktop, tablet, and mobile devices
- **Real-time Updates**: Live notifications and updates using modern web technologies
- **Search & Filter**: Advanced search capabilities with multiple filtering options

## Technology Stack

### Backend Technologies
- **Framework**: Django (Python web framework)
- **API**: Django REST Framework for RESTful API endpoints
- **Database**: PostgreSQL for robust data management
- **Caching**: Redis for high-performance caching and session management
- **Task Processing**: Celery for asynchronous task handling

### Frontend Technologies
- **Styling**: Custom CSS for responsive and modern UI design
- **Templates**: Django template engine for server-side rendering

### Development Tools
- **Code Formatting**: Black for consistent Python code formatting
- **Linting**: Flake8 for code quality assurance
- **Version Control**: Git with pre-commit hooks for code quality

## System Requirements

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database server
- Redis server (for caching and task queue)
- Git for version control

### Hardware Requirements
- Minimum 2GB RAM (4GB recommended)
- 1GB available disk space
- Internet connection for package installation

## Installation Guide

### Step 1: Repository Setup
```bash
# Clone the repository
git clone https://github.com/Mario-Lupo-Ciaponi/vkusiada.git

# Navigate to project directory
cd vkusiada
```

### Step 2: Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Dependency Installation
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 4: Database Configuration
Update the database configuration in your Django settings:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "vkusiada_db",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```

### Step 5: Database Initialization
```bash
# Apply database migrations
python manage.py migrate

# Create administrative user
python manage.py createsuperuser
```

### Step 6: Development Server
```bash
# Start the development server
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Project Structure

```
vkusiada/
├── accounts/                    # User authentication and profile management
│   ├── models.py               # User profile models
│   ├── views.py                # Authentication views
│   └── urls.py                 # URL routing for accounts
├── common/                     # Shared utilities and components
│   ├── utils.py                # Common utility functions
│   └── mixins.py               # Reusable view mixins
├── ingredients/                # Ingredient management system
│   ├── models.py               # Ingredient data models
│   ├── views.py                # Ingredient management views
│   └── serializers.py          # API serializers
├── recipes/                    # Recipe creation and management
│   ├── models.py               # Recipe data models
│   ├── views.py                # Recipe CRUD operations
│   └── admin.py                # Django admin configuration
├── static/                     # Static assets
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── images/                 # Image assets
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── recipes/                # Recipe-related templates
│   └── accounts/               # User account templates
├── vkusiada/                   # Django project configuration
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI application
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── README.md                   # Project documentation
```

## Usage Guide

### For End Users

#### Getting Started
1. **Registration**: Create a new account or log in with existing credentials
2. **Profile Setup**: Complete your user profile with preferences and dietary requirements
3. **Ingredient Inventory**: Add ingredients to your personal pantry for personalized recommendations

#### Recipe Discovery
1. **Browse Categories**: Explore recipes by cuisine type, meal category, or cooking time
2. **Search Function**: Use the search bar to find specific recipes or ingredients
3. **Filter Options**: Apply filters for dietary restrictions, difficulty level, or preparation time

#### Recipe Management
1. **Save Favorites**: Bookmark recipes for easy access later
2. **Create Recipes**: Share your own recipes with the community
3. **Rate & Review**: Provide feedback on recipes you've tried

#### Community Interaction
1. **Comments**: Engage with recipe creators and other users
2. **Profile Connections**: Follow other users and discover their recipe collections
3. **Recipe Sharing**: Share recipes on social media or with friends

### For Developers

#### API Endpoints
- `GET /api/recipes/` - List all recipes
- `POST /api/recipes/` - Create new recipe
- `GET /api/recipes/{id}/` - Retrieve specific recipe
- `PUT /api/recipes/{id}/` - Update recipe
- `DELETE /api/recipes/{id}/` - Delete recipe

#### Authentication
The platform uses Django's built-in authentication system with session-based authentication for web interface and token-based authentication for API access.

#### Custom Management Commands
```bash
# Import sample data
python manage.py loaddata sample_recipes

# Generate recipe thumbnails
python manage.py generate_thumbnails

# Clean up unused media files
python manage.py cleanup_media
```

## API Documentation

### Authentication
Most API endpoints require authentication. Include the authentication token in the request header:
```
Authorization: Token your_api_token
```

### Recipe Endpoints
- **List Recipes**: `GET /api/recipes/`
- **Create Recipe**: `POST /api/recipes/`
- **Recipe Details**: `GET /api/recipes/{id}/`
- **Update Recipe**: `PUT /api/recipes/{id}/`
- **Delete Recipe**: `DELETE /api/recipes/{id}/`

### Ingredient Endpoints
- **List Ingredients**: `GET /api/ingredients/`
- **User Inventory**: `GET /api/ingredients/inventory/`
- **Add to Inventory**: `POST /api/ingredients/inventory/`

## Contributing

We welcome contributions from the community! Here's how you can contribute:

### Development Process
1. **Fork the Repository**: Create your own fork of the project
2. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Make Changes**: Implement your feature or bug fix
4. **Test Changes**: Ensure all tests pass and add new tests if needed
5. **Commit Changes**: `git commit -m 'Add descriptive commit message'`
6. **Push Branch**: `git push origin feature/your-feature-name`
7. **Create Pull Request**: Submit a pull request with a clear description of changes

### Code Standards
- Follow PEP 8 Python style guidelines
- Use Black for code formatting
- Write descriptive commit messages
- Include tests for new features
- Update documentation as needed

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Provide detailed reproduction steps for bugs
- Include system information and error messages when applicable

## License

This project is licensed under the MIT License, which allows for both personal and commercial use. See the [LICENSE](https://opensource.org/license/mit) file for full license text.

## Support

### Live Demo
Experience Vkusiada in action: [Live Demo](https://vkusiada-htfffgfrebc5ezbe.italynorth-01.azurewebsites.net/)

### Contact Information
- **Author**: Mario Lupo Ciaponi
- **GitHub**: [Mario-Lupo-Ciaponi](https://github.com/Mario-Lupo-Ciaponi)
- **Project Repository**: [vkusiada](https://github.com/Mario-Lupo-Ciaponi/vkusiada)

### Getting Help
1. Check the documentation first
2. Search existing GitHub issues
3. Create a new issue with detailed information
4. Join community discussions in the repository
