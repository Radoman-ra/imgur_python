
# Image Upload Service

## Project Overview

This project is a web service for uploading and sharing images, similar to "Imgur". Users can upload multiple images with titles, view posts on a main page, and interact through upvoting or downvoting. It supports user authentication, anonymous posting, and viewing user-specific posts.

## Functional Requirements

### User Authentication

- Registration and login with JWT authentication.
- Authentication required for posting images, voting, and accessing user-specific pages.

### Image Uploads

- Authenticated users can upload 1-N images per post, each with a title.
- Posts displayed on the main page with pagination options (25, 50, 100 posts).

### Voting System

- Authenticated users can upvote or downvote posts.
- Each user can vote only once per post.

### User Profiles

- Authenticated users can view their own posts and vote counts.
- Users can post images anonymously if they have an account.

### Post Details

- Each post has a dedicated page accessible via a unique URL (postId).

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

## Functionality

### Controllers

1. **AuthController**
    - `register_user(request)`: Register a new user.
    - `login_user(request)`: Log in and get JWT token.

2. **ImageController**
    - `upload_image(request)`: Upload images by authenticated users.
    - `get_images(request, limit)`: Retrieve images with pagination.

3. **PostController**
    - `get_post(request, postId)`: Retrieve post details by ID.
    - `get_user_posts(request)`: Retrieve posts by the authenticated user.
    - `create_post(request)`: Create a post with images and a title.

4. **VoteController**
    - `upvote_post(request, postId)`: Upvote a post.
    - `downvote_post(request, postId)`: Downvote a post.

### Services

1. **AuthService**
    - `create_user(data)`: Create a new user.
    - `authenticate_user(credentials)`: Authenticate user and generate JWT tokens.

2. **ImageService**
    - `save_image(data, user)`: Save images and associate them with the user.
    - `fetch_images(limit)`: Fetch images for the main page.

3. **PostService**
    - `get_post_details(postId)`: Retrieve post details.
    - `get_user_posts(user)`: Retrieve user’s posts.

4. **VoteService**
    - `register_vote(postId, user, vote_type)`: Register a vote for a post.

### Models and DTOs

1. **User**
    - `id`: Integer (primary key)
    - `username`: String
    - `password`: String (hashed)
    - `email`: String

2. **Image**
    - `id`: Integer (primary key)
    - `title`: String
    - `image_path`: String
    - `postId`: ForeignKey (Post)

3. **Post**
    - `id`: Integer (primary key)
    - `title`: String
    - `description`: String
    - `images`: ManyToManyField (Image)
    - `upvotes`: Integer (default=0)
    - `downvotes`: Integer (default=0)
    - `userId`: ForeignKey (User)

4. **Vote**
    - `id`: Integer (primary key)
    - `userId`: ForeignKey (User)
    - `postId`: ForeignKey (Post)
    - `vote_type`: String (choices: '1', '-1')

### DTOs

1. **UserDTO**
    - `username`: String
    - `email`: String

2. **ImageDTO**
    - `id`: Integer
    - `title`: String
    - `image_path`: String

3. **PostDTO**
    - `id`: Integer
    - `title`: String
    - `images`: List[ImageDTO]
    - `upvotes`: Integer
    - `downvotes`: Integer

4. **VoteDTO**
    - `postId`: Integer
    - `vote_type`: String

### API Endpoints

- `/api/auth/register`: POST - Register a new user.
- `/api/auth/login`: POST - Login and receive JWT token.
- `/api/images/upload`: POST - Upload images.
- `/api/images`: GET - Get images with pagination.
- `/api/posts/{postId}`: GET - Get post details by ID.
- `/api/user/posts`: GET - Get posts of the authenticated user.
- `/api/votes/upvote/{postId}`: POST - Upvote a post.
- `/api/votes/downvote/{postId}`: POST - Downvote a post.

### URL Configuration

- `/admin/`: Django admin interface.
- `/`: Main page displaying all images.
- `/image/<int:image_id>/`: Detailed view of an image.
- `/home_image/<int:image_id>/`: Alternate detailed view of an image.
- `/image/<int:image_id>/delete/`: Delete an image.
- `/image/<int:image_id>/update/`: Update an image.
- `/api/profile/`: User profile page.
- `/register/`: User registration.
- `/login/`: User login.
- `/logout/`: User logout.
- `/upvote/<int:image_id>/`: Upvote an image.
- `/downvote/<int:image_id>/`: Downvote an image.
- `/swagger/`: Swagger UI for API documentation.
- `/redoc/`: ReDoc UI for API documentation.
- `/api/token/`: JWT token obtain endpoint.
- `/api/token/refresh/`: JWT token refresh endpoint.
- `/profile/`: Redirects to home page.

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
