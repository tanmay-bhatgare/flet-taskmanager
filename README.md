# Flet Task Manager (v2)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend) -[UI](#ui)
- [Acknowledgments](#acknowledgments)

## Introduction

Flet Task Manager is a comprehensive task management application designed to help individuals, track, and manage their tasks efficiently. Built with a robust backend and an intuitive frontend, the application ensures seamless interaction and real-time updates.

## Features

- **User Authentication:** Secure login and signup functionality using OAuth2.
- **Task Management:** Create, update, delete, and view tasks with ease.
- **Real-time Updates:** Instant synchronization between frontend and backend.
- **Responsive UI:** Intuitive and user-friendly interface built with Flet.
- **Session Management:** Efficient handling of user sessions and tokens.
- **Error Handling:** Robust error management and feedback mechanisms using `icecream`.

## Directory Structure

```bash
flet-taskmanager
    ├── backend
    │   ├── app
    │   │   ├── __init__.py
    │   │   ├── authentication
    │   │   │   ├── __init__.py
    │   │   │   └── oauth2.py
    │   │   ├── configuration
    │   │   │   └── config.py
    │   │   ├── db
    │   │   │   ├── __init__.py
    │   │   │   └── database.py
    │   │   ├── main.py
    │   │   ├── models
    │   │   │   ├── __init__.py
    │   │   │   ├── taskModel.py
    │   │   │   └── userModel.py
    │   │   ├── routes
    │   │   │   ├── authRoutes.py
    │   │   │   ├── taskRoutes.py
    │   │   │   └── userRoutes.py
    │   │   ├── schemas
    │   │   │   ├── __init__.py
    │   │   │   ├── taskSchema.py
    │   │   │   ├── tokenSchema.py
    │   │   │   └── userSchema.py
    │   │   └── utils
    │   │       ├── __init__.py
    │   │       ├── limiter.py
    │   │       └── utils.py
    │   │── .gitignore
    │   │── .env # need to add manually
    │   └── requirements.txt
    └── frontend
        ├── __init__.py
        ├── assets
        │   └── icon.png
        ├── constants
        │   ├── __init__.py
        │   ├── constants.py
        │   ├── pallet.py
        │   ├── routes.py
        │   ├── session_key.py
        │   ├── urls.py
        │   └── widget_style.py
        ├── controllers
        │   ├── __init__.py
        │   ├── controllers.py
        │   ├── login_controller.py
        │   ├── sign_up_controller.py
        │   └── task_controller.py
        ├── main.py
        ├── models
        │   ├── __init__.py
        │   ├── login_model.py
        │   ├── models.py
        │   ├── sign_up_model.py
        │   └── task_model.py
        ├── requirements.txt
        ├── utils
        │   ├── __init__.py
        │   ├── date_converter.py
        │   ├── field_error_updater.py
        │   ├── jwt_token_encoder.py
        │   ├── session_storage_setter.py
        │   └── view_handler.py
        ├── views
        │   ├── __init__.py
        │   ├── home_view.py
        │   ├── login_view.py
        │   ├── sign_up_view.py
        │   └── views.py
        └── widgets
            ├── __init__.py
            ├── pop_up_task_card.py
            ├── task_card.py
            └── widgets.py

```

## Technologies Used

### Backend

- **Python**: Core programming language.
- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for database interactions.
- **OAuth2**: Authentication protocol.
- **Pydantic**: Data validation and settings management.

### Frontend

- **Python**: Core programming language.
- **Flet**: Framework for building interactive UI applications.
- **JWT**: JSON Web Tokens for authentication.
- **Custom Widgets**: Reusable UI components for consistency.

## Installation

### Prerequisites

- **Python 3.9+**: Ensure Python is installed on your machine.
- **pip**: Python package installer.
- **Git**: Version control system.

### Backend Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/flet-taskmanager.git
   cd flet-taskmanager/backend
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv .venv
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # Linux or Mac

   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt # use pip3 if this fails
   ```
4. **Setup Environment Variables**

   - Make a .env file in backend directory
   - Configure it:

     ```bash
        DATABASE_HOSTNAME = <value> # The hostname your database is running, default(localhost)
        DATABASE_PORT = <value> # The port your server is running on, default(5432)
        DATABASE_NAME = <value> # The name of your DB.
        DATABASE_USERNAME = <value> # The username of your Postgres, default(postgres)
        DATABASE_PASSWORD = <value> # The Password of your DB
        SECRET_KEY = <value> # 32 bits encoding for JWT tokens
        ALGORITHMS = <value> # The algorithm used for JWT signature.
        ACCESS_TOKEN_EXPIRE_MINUTES = <value> # The time for each JWT to expire(in minutes).
     ```

### Frontend Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/flet-taskmanager.git
   cd flet-taskmanager/frontend
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv .venv
   # Activate Environment
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # Linux or Mac

   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt # use pip3 if this fails
   ```

### Usage

## Running the Backend

1. **Navigate to Backend Directory**

   ```bash
   cd flet-taskmanager/backend
   # activate virtual environment
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # Linux or Mac

   ```

2. **Run FastAPI Server**
   ```bash
   uvicorn app.main:app --port 8000
   ```
   - API will be exposed on http://localhost:8000

## Running the Frontend

1. **Navigate to Frontend Directory**

   ```bash
   cd flet-taskmanager/frontend
   # activate virtual environment
   .venv/Scripts/activate  # Windows
   source .venv/bin/activate  # Linux or Mac

   ```

2. **Run Flet App**
   ```bash
   flet run --web --port 8080 # Make sure you don't have any other service running on port you provided.
   ```

## Acknowledgments

I would like to thank the following people for their contributions and support:

- **[Feodor Fitsner](https://github.com/FeodorFitsner)** for introducing `Flet`, and simplifying frontend development for Python backend developers.

## UI

## Home View

![Home View](/frontend/assets/images/home_view.jpg)

## Sign In View

![Home View](/frontend/assets/images/login_view.jpg)

## Sign Up View

![Home View](/frontend/assets/images/sign_up_view.jpg)
