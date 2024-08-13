
# Image Upload Service

## Project Overview

This project is a web service for uploading and sharing images, similar to "Imgur". Users can upload multiple images with titles, view posts on a main page, and interact through upvoting or downvoting. It supports user authentication, anonymous posting, and viewing user-specific posts.

## Functional Requirements

### User Authentication

- Registration and login with JWT authentication.
- Authentication required for posting images, voting, and accessing user-specific pages.

### Image Uploads

- Authenticated users can upload 1-N images per post, each with a title.

### Voting System

- Authenticated users can upvote or downvote posts.
- Each user can vote only once per post.

### User Profiles

- Authenticated users can view their own posts and vote counts.

## Technical Specifications

### Prerequisites

- Python virtual environment (`venv`)
- Decorators

### Tech Stack

- Django (backend framework)
- Swagger (API documentation)
- MySQL (database)
- Docker (containerization)
- JWT Auth (authentication)

## How to Use

### Setting Up the Environment

1. **Create a `.env` File**

   Create a `.env` file in the `./imgur` directory with the following content, replacing placeholder values with your own:

   ```ini
   MYSQL_ROOT_PASSWORD=your_mysql_root_password
   MYSQL_DATABASE=imgur_db
   MYSQL_USER=mysql
   MYSQL_PASSWORD=your_mysql_password

   DATABASE_NAME=imgur_db
   DATABASE_USER=mysql
   DATABASE_PASSWORD=your_mysql_password
   DATABASE_HOST=127.0.0.1
   DATABASE_PORT=3306

   SECRET_KEY="your_django_secret_key"
   DEBUG=True

   ALLOWED_HOSTS="localhost,127.0.0.1"
   CSRF_TRUSTED_ORIGINS="https://your-domain.com"
   ```

2. **Run Docker Compose**

   Navigate to the `./imgur` directory and run the following command to build and start the Docker container:

   ```bash
   docker-compose up --build
   ```

## Additional Information

- **Virtual Environment**: Ensure a Python virtual environment is set up for dependency management.
- **Decorators**: Use decorators for functions such as authentication and request validation.
- **Swagger**: Implement Swagger for API documentation to enable easy testing and interaction with the API.

This README provides instructions to set up and run the Image Upload Service. Follow these guidelines to effectively deploy and use the application.
