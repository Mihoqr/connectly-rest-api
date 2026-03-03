# Connectly API - Enhancing the API with Design Patterns

This repository contains the enhanced version of the Connectly API, focusing on the implementation of **Singleton** and **Factory** design patterns to improve code modularity, scalability, and maintainability.

## 🛠️ Design Patterns Implemented

### 1. Singleton Pattern
We used the Singleton pattern to ensure that specific classes have only one instance and provide a global point of access to them.
* **ConfigManager**: Centralizes all API configurations (e.g., pagination settings, rate limits) to ensure consistency across the application.
* **LoggerSingleton**: A centralized logging utility used for tracking API initializations and recording errors during the post-creation process.

### 2. Factory Pattern
The Factory pattern was implemented to standardize the creation of `Post` objects.
* **PostFactory**: A dedicated class responsible for instantiating different post types (Text, Image, Video).
* **Validation Logic**: Enforces specific metadata requirements during object creation:
    * **Image Posts**: Requires `file_size` in the metadata.
    * **Video Posts**: Requires `duration` in the metadata.

## 📂 Structural Changes
To improve project organization, the directory structure has been flattened:
* `/factories`: Contains `post_factory.py`.
* `/singletons`: Contains `config_manager.py` and `logger_singleton.py`.
* Root Directory: Main Django configuration and app files for easier access.

## 🧪 Testing and Validation (Postman)
The Factory logic and API endpoints were validated using Postman. Below are the test scenarios conducted:

| Scenario | Post Type | Metadata Status | Expected Result | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| **Pass** | Image | `{"file_size": "2MB"}` | Post created successfully | `201 Created` |
| **Pass** | Video | `{"duration": "05:00"}` | Post created successfully | `201 Created` |
| **Fail** | Image | Missing `file_size` | Error: Image posts require file_size | `400 Bad Request` |
| **Fail** | Video | Missing `duration` | Error: Video posts require duration | `400 Bad Request` |



## 🚀 Getting Started

1. **Clone and Navigate**:
   ```bash
   git clone <https://github.com/Mihoqr/connectly-rest-api.git>
   cd Connectly_Final_Rebuild
