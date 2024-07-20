# Technical Specification: Image Upload Service (Analogue to "Imgur")

## Project Overview

The objective of this project is to create a web service similar to "Imgur," where users can upload and share images. The service will handle user authentication, allowing users to upload multiple photos as posts, with titles, and view them on a main page. Users can also upvote or downvote posts, view their own posts and their respective upvote/downvote counts, and post anonymously if they have an account.

## Functional Requirements

### User Authentication

- Users should be able to register and log in using JWT authentication.
- Authentication should be required for posting images, voting, and accessing user-specific pages.

### Image Uploads

- Authenticated users can upload 1-N images per post, each with a title.
- Posts should be displayed on a main page with options to choose the number of posts displayed (25, 50, 100).

### Voting System

- Authenticated users can upvote or downvote posts on the main page.
- Votes should be unique per user per post.

### User Profiles

- Authenticated users can view a list of their own posts and the upvote/downvote counts for each.
- Users can post images anonymously.

### Post Details

- Each post should have its own dedicated page accessible via a unique URL (postId).

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
   - `register_user(request)`: Handles user registration.
   - `login_user(request)`: Handles user login and JWT token issuance.

2. **ImageController**
   - `upload_image(request)`: Handles image uploads by authenticated users.
   - `get_images(request, limit)`: Retrieves a list of images for the main page, with pagination support (25, 50, 100 posts).

3. **PostController**
   - `get_post(request, postId)`: Retrieves details of a specific post by its ID.
   - `get_user_posts(request)`: Retrieves posts uploaded by the authenticated user.
   - `create_post(request)`: Allows authenticated users to upload images and title for post.

4. **VoteController**
   - `upvote_post(request, postId)`: Handles upvoting a post.
   - `downvote_post(request, postId)`: Handles downvoting a post.

### Services

1. **AuthService**
   - `create_user(data)`: Creates a new user.
   - `authenticate_user(credentials)`: Authenticates user credentials and generates JWT tokens.

2. **ImageService**
   - `save_image(data, user)`: Saves uploaded images and associates them with the user.
   - `fetch_images(limit)`: Fetches images for the main page with the specified limit.

3. **PostService**
   - `get_post_details(postId)`: Retrieves detailed information about a specific post.
   - `get_user_posts(user)`: Retrieves posts created by the user.

4. **VoteService**
   - `register_vote(postId, user, vote_type)`: Registers an upvote or downvote for a post.

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

## Additional Information

- **Virtual Environment**: Ensure a Python virtual environment is set up for dependency management.
- **Decorators**: Utilize decorators for functions such as authentication and request validation.
- **Swagger**: Implement Swagger for API documentation to enable easy testing and interaction with the API.
- **Docker**: Use Docker for containerizing the application, ensuring consistency across different environments.

This specification outlines the key components and functionalities required to develop an image upload service similar to "Imgur." By following this spec, the project will deliver a robust and scalable web application that meets the outlined requirements.