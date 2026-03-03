# Connectly REST API - Milestone 1 and Milestone 2 (Full Implementation)

This repository contains the complete implementation of Milestone 1 and Milestone 2 for the Connectly REST API. The project has been evolved from a basic CRUD setup to a secure, pattern-driven system designed for scalability and maintainability.

## Project Architecture
The project structure has been refactored into a "flattened" modular layout to improve accessibility and follow industry best practices:
* **`/factories`**: Standardized object creation using the Factory Pattern.
* **`/singletons`**: Centralized configuration and logging services.
* **`/posts`**: Main application logic for post and comment management.
* **`/connectly_project`**: Core Django settings and authentication configurations.



##  Key Features

### 1. Design Patterns
* **Factory Pattern**: Implemented `PostFactory` to handle logic for Text, Image, and Video posts. It enforces strict metadata validation (e.g., `file_size` for images and `duration` for videos).
* **Singleton Pattern**: Created `ConfigManager` for global API settings and `LoggerSingleton` for consistent system-wide event logging.

### 2. API Security & Authentication
* **Token-Based Authentication**: Secured endpoints using Django REST Framework's Token system.
* **Advanced Hashing**: Implemented Argon2 and PBKDF2 for robust password protection.
* **SSL/HTTPS**: Configured support for secure data transmission using SSL certificates (`cert.pem`, `key.pem`).

### 3. Core CRUD Functionality
* Robust endpoints for User registration, Authentication, and Post management.
* Detailed validation for all incoming JSON requests.

### 4. User Interactions (Like and Comment) 
### Like Functionality
Users can now like posts. Each user is only allowed to like a specific post once.  
The system prevents duplicate likes and returns proper error responses if:
- The post does not exist (404)
- The user already liked the post (400)

Endpoint:
POST /posts/{id}/like/

### Comment Functionality
Users can now add comments to posts and retrieve comments per post.  
Each comment is automatically linked to:
- The logged-in user
- The specific post (via URL parameter)

Endpoints:
POST /posts/{id}/comment/
GET /posts/{id}/comments/

Validation ensures:
- Comments cannot be added to non-existent posts
- Proper error handling is returned when needed

---

### Like & Comment Count
The post detail endpoint was updated to include:
- like_count
- comment_count

This allows clients to easily see how many likes and comments a post has.

---

### Google OAuth Login
Integrated Google OAuth to allow users to log in using their Google account.

Endpoint:
POST /auth/google/login/

The backend:
1. Verifies the Google ID token
2. Extracts the user email
3. Creates a user if not existing
4. Generates a DRF authentication token

Proper error handling is included for invalid or expired tokens.

### Postman Validation
The API has been fully verified using Postman with the following test suite:
1. **User Auth**: Register -> Login -> Token Retrieval.
2. **Factory Pass**: Successfully created Image/Video posts with correct metadata.
3. **Validation Fail**: Correctly caught `400 Bad Request` errors when required metadata fields were missing.

### Integrating Third-Party Services 
	•	Client secrets are not stored in the repository.
	•	Google OAuth credentials are managed securely in Google Cloud Console.
	•	Sensitive information is excluded from version control.

This project was developed collaboratively by the team.

AI tools (including ChatGPT) were used as a learning assistant to:
- Clarify OAuth integration steps


## Link For Design Patterns
<https://drive.google.com/drive/folders/17-shjiSjsrdfu2VWXNm7dRurJkm0SRZN?usp=sharing>

##  Setup and Installation

1. **Activate Virtual Environment**:
   ```bash
   source env/Scripts/activate


## Diagrams

## Entity Relationship Diagram
```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ COMMENT : writes
    USER ||--o{ LIKE : gives
    POST ||--o{ COMMENT : receives
    POST ||--o{ LIKE : receives

    USER {
        int id PK
        string username UK
        string email UK
        string password
        datetime date_joined
    }

    POST {
        int id PK
        string title
        text content
        string post_type
        json metadata
        int author_id FK
        datetime created_at
    }

    COMMENT {
        int id PK
        text text
        int author_id FK
        int post_id FK
        datetime created_at
    }

    LIKE {
        int id PK
        int user_id FK
        int post_id FK
        datetime created_at
        string unique_constraint "user_id, post_id"
    }


## CRUD Operations Flow

```mermaid
flowchart TD
    A[User Registers] --> B[User Logs In]
    B --> C[API Returns Auth Token]
    C --> D[Create Post]
    D --> E[Post Stored in Database]
    C --> F[Like Post]
    F --> G{Already Liked?}
    G -->|No| H[Save Like]
    G -->|Yes| I[Return 400 Error]
    C --> J[Comment on Post]
    J --> K{Post Exists?}
    K -->|Yes| L[Save Comment]
    K -->|No| M[Return 400 Error]
    E --> N[Retrieve Post Details]
    H --> N
    L --> N
```

