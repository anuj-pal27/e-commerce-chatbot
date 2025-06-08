# Quick Setup Guide - Django Chatbot Project

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git (for cloning)

## Step 1: Clone the Repository
```bash
git clone <repository-url>
cd django-chatbot
```

## Step 2: Backend Setup (Django)

### Create Virtual Environment
```bash
python -m venv .venv

# Activate virtual environment
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### Install Dependencies
```bash
cd firstproject
pip install django djangorestframework django-cors-headers requests
```

### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User
```bash
python manage.py createsuperuser
```

### Populate with Mock Data
```bash
python populate_products.py
```

### Start Backend Server
```bash
python manage.py runserver
```
Backend will run on: http://localhost:8000

## Step 3: Frontend Setup (React)

### Open New Terminal and Navigate to Frontend
```bash
cd chatbot_frontend
```

### Install Dependencies
```bash
npm install
```

### Start Frontend Development Server
```bash
npm run dev
```
Frontend will run on: http://localhost:5173

## Step 4: Test the Application

1. Open browser and go to http://localhost:5173
2. Register a new user account
3. Login and start chatting with the bot
4. Try queries like:
   - "Show me laptops"
   - "I need cheap electronics"
   - "Find products under $50"
   - "Help"

## Admin Panel Access
- URL: http://localhost:8000/admin/
- Use the superuser credentials created in Step 2

## API Documentation
- Base URL: http://localhost:8000/api/
- See PROJECT_DOCUMENTATION.md for complete API reference

## Troubleshooting

### Common Issues:
1. **Port conflicts**: Change ports in settings if needed
2. **CORS errors**: Ensure CORS_ALLOWED_ORIGINS includes frontend URL
3. **Module not found**: Ensure virtual environment is activated
4. **Database errors**: Run migrations again

### Reset Database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python populate_products.py
```

## Development Tools

### Django Admin
- Manage products, users, and chat sessions
- URL: http://localhost:8000/admin/

### API Testing
- Use tools like Postman or curl
- All endpoints documented in PROJECT_DOCUMENTATION.md

## Next Steps
- Read PROJECT_DOCUMENTATION.md for detailed architecture
- Customize the chatbot responses in `chatbot_service.py`
- Add more product categories and data
- Implement additional features as needed 