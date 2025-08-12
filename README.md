# 🧠 AI Chat Token-Based API

A **Django REST Framework** backend for a token-based AI chat system.  
Users can register, log in to receive an authentication token, send messages to the AI, and track their remaining token balance.

---

## 🚀 Features
- **User Registration & Login** (with password hashing)
- **Custom Token-Based Authentication** (not DRF default)
- **Token Balance Tracking** (each chat deducts tokens)
- **Chat History Storage** (message + AI response)
- **Simple AI Response** (demo: echoes user input)
- **REST API with JSON Responses**

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/aichat.git
cd aichat
```
2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
4️⃣ Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```
5️⃣ Start the Development Server
```
python manage.py runserver
```
Server will be available at:
📍 http://127.0.0.1:8000/
🔑 API Endpoints
POST	/api/register/
POST	/api/login/
POST	/api/chat/
GET	/api/tokens/
📌 Example Usage (with curl)
1️⃣ Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123"}'
```
Response:
```bash
{"message": "User registered successfully", "tokens": 4000}
```
2️⃣ Login
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123"}'
```
Response:
```
{"message": "Login successful", "token": "abc123...", "tokens_left": 4000}
```
3️⃣ Chat with AI
```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123..." \
  -d '{"message": "Hello AI"}'
```
Response:
```
{"message": "Hello AI", "response": "AI says: You said 'Hello AI'", "tokens_left": 3900}
```
4️⃣ Check Token Balance
```bash
curl -X GET http://127.0.0.1:8000/api/tokens/ \
  -H "Authorization: Token abc123..."
```
Response:
```
{"tokens_left": 3900}
```
## ⚠️ Challenges Faced
- Token Authentication Conflict – DRF’s built-in TokenAuthentication conflicted with the custom AuthToken model.
- Solution: Removed DEFAULT_AUTHENTICATION_CLASSES from settings.py to fully rely on custom authentication.
- curl Authorization Issues – The "Authorization: Token <key>" format must be exact; missing prefix or spacing caused "Invalid token" errors.
- Token Deduction Race Conditions – Token deduction logic was adjusted to ensure atomic updates when saving user data.

## 💡 Suggestions for Improvement
- Replace the dummy AI response with integration to a real AI API (OpenAI, Hugging Face, etc.)
- Add refresh tokens & expiry for improved security
- Implement pagination & search in chat history
- Add unit tests for all endpoints
- Use signals to handle token creation on registration
