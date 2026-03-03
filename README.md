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

### 5. Integrating Third-Party Services (Google OAuth Login)
Integrated Google OAuth to allow users to log in using their Google account.

Endpoint:
POST /auth/google/login/

The backend:
1. Verifies the Google ID token
2. Extracts the user email
3. Creates a user if not existing
4. Generates a DRF authentication token

Proper error handling is included for invalid or expired tokens.

### 6. News Feed 
### Endpoint: GET /posts/feed/

This endpoint retrieves posts sorted by newest first and applies pagination.

Features:
- Requires Token Authentication
- Sorted by `created_at` (descending)
- Pagination enabled (default page size = 5)
- Handles invalid page requests gracefully

### Example Successful Response

```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [...]
}
```

### Example Error Response

```json
{
    "detail": "Invalid page."
}
```

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

## 1. Entity Relationship Diagram
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
```


## 2. CRUD Operations Flow

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

    C --> O[GET /posts/feed/]
    O --> P[Sort by -created_at]
    P --> Q[Apply Pagination]
    Q --> R[Return Paginated Feed]

    E --> R
    H --> R
    L --> R
```

## 3. System Architecture Diagram

```mermaid
graph TB
    subgraph Client["Client Layer"]
        Postman["Postman / Frontend Client"]
    end

    subgraph API["API Layer"]
        Router["URL Router<br/>connectly_project/urls.py"]
        Views["API Views<br/>posts/views.py"]
    end

    subgraph Auth["Authentication & Authorization"]
        TokenAuth["TokenAuthentication"]
        Permissions["IsAuthenticated"]
        GoogleOAuth["Google OAuth Login"]
    end

    subgraph Processing["Data Processing"]
        Serializers["Serializers<br/>posts/serializers.py"]
        Factory["PostFactory<br/>Factory Pattern"]
        Pagination["Pagination<br/>PageNumberPagination"]
        Sorting["Sorting Logic<br/>order_by(-created_at)"]
    end

    subgraph Models["Data Models"]
        ModelLayer["User, Post, Comment, Like<br/>posts/models.py"]
    end

    subgraph Utils["Utilities"]
        Logger["LoggerSingleton"]
        Config["ConfigManager"]
    end

    subgraph Storage["Storage Layer"]
        DB["SQLite Database<br/>db.sqlite3"]
    end

    Postman -->|HTTP Request| Router
    Router -->|Route Request| Views

    Views -->|Authenticate| TokenAuth
    Views -->|Permission Check| Permissions
    Views -->|Google Login| GoogleOAuth

    Views -->|Validate Data| Serializers
    Views -->|Create Post| Factory

    Views -->|Apply Sorting| Sorting
    Views -->|Apply Pagination| Pagination

    Serializers -->|Interact| ModelLayer
    Factory -->|Interact| ModelLayer
    ModelLayer -->|Query & Persist| DB

    Views -->|Log Events| Logger
    Logger -->|Read Settings| Config

    Views -->|JSON Response| Postman

    style Client fill:#e1f5ff
    style API fill:#f3e5f5
    style Auth fill:#fff3e0
    style Processing fill:#e8f5e9
    style Models fill:#fce4ec
    style Utils fill:#f1f8e9
    style Storage fill:#ede7f6
```

## 4. API Request/Response Flow

```mermaid
sequenceDiagram
    participant Client as Client / Postman
    participant Router as URL Router
    participant View as Django View
    participant Auth as TokenAuthentication
    participant Perms as IsAuthenticated
    participant Serializer as Serializer
    participant Factory as PostFactory
    participant Model as Models (User, Post, Comment, Like)
    participant DB as SQLite Database

    Client->>Router: HTTP Request + Token
    Router->>View: Route to View

    View->>Auth: Validate Token
    alt Token Invalid
        Auth-->>Client: 401 Unauthorized
    else Token Valid
        Auth->>View: Authenticated User

        View->>Perms: Check Permission
        alt Permission Denied
            Perms-->>Client: 403 Forbidden
        else Permission Granted

            View->>Serializer: Validate Request Data
            alt Validation Fails
                Serializer-->>Client: 400 Bad Request
            else Validation Passes
                Serializer->>View: Validated Data

                alt Create Post
                    View->>Factory: Create Post (Factory Pattern)
                    Factory->>Model: Prepare Model Object
                else Other CRUD / Feed
                    View->>Model: Execute Business Logic
                end

                Model->>DB: Query / Insert / Update / Delete
                DB-->>Model: Result
                Model-->>View: Data Object

                View-->>Client: 200 / 201 / 204 JSON Response
            end
        end
    end
```


## 5. Google OAuth Login Flow

```mermaid
sequenceDiagram
    participant Client as Client / Postman
    participant Google as Google OAuth Server
    participant API as Django API
    participant GoogleLib as google-auth Library
    participant UserModel as User Model
    participant DB as SQLite Database
    participant Token as DRF Token System

    Client->>Google: Request Authorization Code
    Google-->>Client: Authorization Code

    Client->>Google: Exchange Code for Tokens
    Google-->>Client: id_token + access_token

    Client->>API: POST /auth/google/login<br/>with id_token

    API->>GoogleLib: Verify id_token
    alt Invalid or Expired Token
        GoogleLib-->>API: Verification Failed
        API-->>Client: 400 Invalid Token
    else Valid Token
        GoogleLib-->>API: Decoded User Info (email, name)

        API->>UserModel: Check if User Exists
        alt User Not Found
            UserModel->>DB: Create New User
        else User Exists
            UserModel->>DB: Retrieve User
        end

        DB-->>UserModel: User Object

        API->>Token: Generate or Retrieve Auth Token
        Token->>DB: Store/Retrieve Token
        DB-->>Token: Token Value

        API-->>Client: 200 OK + DRF Token
    end
```
