# Connectly API - Activity 6: Data Handling

This branch contains the completed implementation for **Activity 6**, focusing on **Data Validation** and **Database Relationships** using Django REST Framework.

## 🚀 Features Implemented
* **User Validation**: Ensures unique usernames and valid email formats using `UserSerializer`.
* **Post-Author Relationship**: Connected posts to users using a Foreign Key relationship.
* **Comment System**: Implemented a new model for comments, linked to both Users and Posts.
* **CSRF Exemption**: Configured Class-Based Views (CBVs) with `@method_decorator` to allow API testing via Postman.

## 🛠️ API Endpoints Tested
| Endpoint | Method | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `/posts/users/` | POST | Creates a new user with validation | 201 Created |
| `/posts/posts/` | POST | Creates a post linked to an author | 201 Created |
| `/posts/comments/` | POST | Creates a comment for a specific post | 201 Created |
| `/posts/posts/` | GET | Retrieves all posts with nested comments | 200 OK |

## 🧪 Testing
The API was verified using **Postman**. The collection has been exported and included in the submission folder as per Step 8 requirements.
