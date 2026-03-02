# Enhancing API Security (Connectly Project)

This repository contains the security-enhanced version of the Connectly API, focusing on data protection, secure transmission, and role-based access control.

## 🚀 Verified Security Features

### 1. Data Encryption (Password Hashing)
- **Status:** Verified ✅
- **Details:** User passwords are never stored in plain text. We utilize Django's `pbkdf2_sha256` hashing algorithm.
- **Proof:** Verified via terminal shell where `print(user.password)` returns a hashed string.

### 2. Secure Data Transmission (HTTPS)
- **Status:** Verified ✅
- **Details:** The API is configured to run over HTTPS to ensure that all data exchanged between the client (Postman) and server is encrypted in transit.
- **Proof:** All API endpoints are accessed via `https://127.0.0.1:8000/`.

### 3. Token-Based Authentication
- **Status:** Verified ✅
- **Details:** Access to protected resources (Posts/Comments) requires a valid `Authorization: Token <7d6564191a2a2aba77012a4f49b01da4449d9287>` header.
- **Proof:** Unauthorized requests return a `401 Unauthorized` response.

### 4. Role-Based Access Control (RBAC)
- **Status:** Verified ✅
- **Details:** Implemented custom permissions (`IsPostAuthor`) to ensure that only the creator of a post can edit or delete it.
- **Proof:** Attempting to delete a post owned by another user returns a `403 Forbidden` status.

## 🛠️ How to Test
1. **Clone the repository** and navigate to the `api-security-branch`.
2. **Activate the virtual environment** and run the server.
3. **Use the provided Postman Collection** (found in the Google Drive submission) to run the following tests:
   - `POST /posts/users/` (Create User)
   - `POST /api-token-auth/` (Obtain Token)
   - `DELETE /posts/posts/<id>/` (Test RBAC - expect 403 if not author)

---
*Developed as part of the Web Development Frameworks course.*
