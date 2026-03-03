# Connectly REST API - Milestone 1 (Full Implementation)

This repository contains the complete implementation of Milestone 1 for the Connectly REST API. The project has been evolved from a basic CRUD setup to a secure, pattern-driven system designed for scalability and maintainability.

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

##  Postman Validation
The API has been fully verified using Postman with the following test suite:
1. **User Auth**: Register -> Login -> Token Retrieval.
2. **Factory Pass**: Successfully created Image/Video posts with correct metadata.
3. **Validation Fail**: Correctly caught `400 Bad Request` errors when required metadata fields were missing.

<https://drive.google.com/drive/folders/17-shjiSjsrdfu2VWXNm7dRurJkm0SRZN?usp=sharing>

##  Setup and Installation

1. **Activate Virtual Environment**:
   ```bash
   source env/Scripts/activate
