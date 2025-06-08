# 🤖 Django E-commerce Chatbot

A full-stack intelligent e-commerce chatbot application built with Django and React that helps users discover and search products through natural language conversations.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-v5.2.2-green.svg)
![React](https://img.shields.io/badge/react-v19.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Chatbot Capabilities](#chatbot-capabilities)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project demonstrates a modern full-stack web application featuring an intelligent chatbot that assists users in finding products through natural language queries. The system maintains conversation history, provides personalized recommendations, and offers advanced search capabilities across multiple product categories.

### Why This Project?

- **Learning Full-Stack Development**: Combines backend API development with modern frontend frameworks
- **Natural Language Processing**: Implements rule-based chatbot logic for product discovery
- **Real-World Application**: Simulates actual e-commerce chat support systems
- **Modern Tech Stack**: Uses current industry-standard tools and frameworks

## ✨ Features

### 🔐 User Management
- **User Registration & Authentication**: Secure user accounts with session management
- **Persistent Chat Sessions**: Conversation history saved per user
- **User Profiles**: Personal account management

### 🤖 Intelligent Chatbot
- **Natural Language Understanding**: Processes user queries in plain English
- **Product Search**: Find products by name, category, or description
- **Price Filtering**: Search within specific price ranges
- **Category Browsing**: Explore products by categories (electronics, fashion, home, etc.)
- **Contextual Responses**: Personalized recommendations based on user queries

### 📱 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Chat Interface**: Smooth conversation experience
- **Product Display**: Rich product cards with images, ratings, and pricing
- **Dashboard**: User-friendly interface for managing chat sessions

### 🛠 Admin Features
- **Django Admin Panel**: Manage products, users, and chat data
- **Product Management**: Full CRUD operations for product catalog
- **Analytics**: View chat sessions and user interactions

## 🛠 Technology Stack

### Backend
- **[Django 5.2.2](https://www.djangoproject.com/)** - Python web framework
- **[Django REST Framework](https://www.django-rest-framework.org/)** - API development toolkit
- **[SQLite](https://www.sqlite.org/)** - Lightweight database for development
- **[CORS Headers](https://github.com/adamchainz/django-cors-headers)** - Cross-origin resource sharing

### Frontend
- **[React 19.1.0](https://reactjs.org/)** - UI framework for building interactive interfaces
- **[Vite 6.3.5](https://vitejs.dev/)** - Fast build tool and development server
- **[TailwindCSS 4.1.8](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Axios 1.9.0](https://axios-http.com/)** - HTTP client for API requests
- **[React Router 7.6.2](https://reactrouter.com/)** - Client-side routing

### Development Tools
- **[ESLint](https://eslint.org/)** - Code linting and quality assurance
- **[DummyJSON API](https://dummyjson.com/)** - Mock data source for products

## 🏗 Architecture

```
┌─────────────────┐    HTTP/REST     ┌─────────────────┐
│  React Frontend │ ◄──────────────► │  Django Backend │
│  (Port 5173)    │    API Calls     │  (Port 8000)    │
└─────────────────┘                  └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  SQLite Database│
                                    │   (db.sqlite3)  │
                                    └─────────────────┘
```

### Key Components
- **Frontend**: React SPA with component-based architecture
- **Backend**: Django REST API with session-based authentication
- **Database**: Relational database with models for users, products, and chat sessions
- **Chatbot Engine**: Rule-based NLP service for processing user queries

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd django-chatbot
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
cd firstproject
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Load sample data
python populate_products.py

# Start backend server
python manage.py runserver
```

### 3. Frontend Setup
```bash
# In a new terminal
cd chatbot_frontend
npm install
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

## 📖 Detailed Setup

For comprehensive setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

### Virtual Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### Database Configuration
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Populate with 100 sample products
python populate_products.py
```

## 💡 Usage

### For End Users

1. **Register**: Create a new account or login with existing credentials
2. **Start Chatting**: Navigate to the chat interface and begin a conversation
3. **Search Products**: Use natural language queries like:
   - "Show me laptops under $500"
   - "I need wireless headphones"
   - "Find cheap electronics"
   - "What beauty products do you have?"

### Sample Chat Interactions

```
User: "Hi there!"
Bot: "Hello! I'm here to help you find the perfect products. What are you looking for today?"

User: "I need a laptop for programming"
Bot: "Here are some great laptop options for programming:
🔸 MacBook Pro 16" - $2399 - Rating: 4.8/5.0
🔸 Dell XPS 15 - $1299 - Rating: 4.6/5.0
..."

User: "Show me something cheaper"
Bot: "Here are some budget-friendly laptop options under $800:
🔸 Acer Aspire 5 - $579 - Rating: 4.2/5.0
..."
```

### For Developers

1. **Admin Panel**: Access Django admin at http://localhost:8000/admin/
2. **API Testing**: Use tools like Postman to test API endpoints
3. **Database Management**: Use Django ORM or admin interface
4. **Customization**: Modify chatbot responses in `firstproject/testapp/chatbot_service.py`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register/` | POST | User registration |
| `/login/` | POST | User login |
| `/logout/` | POST | User logout |
| `/profile/` | GET | Get user profile |

### Product Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products/` | GET | List all products |
| `/products/{id}/` | GET | Get product details |
| `/product-search/` | POST | Advanced product search |

### Chat Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat-sessions/` | GET, POST | Manage chat sessions |
| `/chat-sessions/{id}/messages/` | GET, POST | Chat messages |
| `/chat-sessions/{id}/reset/` | POST | Reset chat session |

### Sample API Request
```bash
# Search for products
curl -X POST http://localhost:8000/api/product-search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "laptop", "max_price": 1000}'
```

For complete API documentation, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md).

## 📁 Project Structure

```
django-chatbot/
├── firstproject/                 # Django Backend
│   ├── firstproject/            # Project Configuration
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Main URL routing
│   │   └── wsgi.py              # WSGI configuration
│   ├── testapp/                 # Main Application
│   │   ├── models.py            # Database models
│   │   ├── views.py             # API views
│   │   ├── serializers.py       # DRF serializers
│   │   ├── chatbot_service.py   # Chatbot logic
│   │   └── populate_products.py # Data population script
│   ├── requirements.txt         # Python dependencies
│   └── manage.py                # Django management
├── chatbot_frontend/            # React Frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API services
│   │   └── App.jsx              # Main app component
│   ├── package.json             # Node dependencies
│   └── vite.config.js           # Vite configuration
├── PROJECT_DOCUMENTATION.md     # Detailed technical docs
├── SETUP_GUIDE.md               # Installation guide
└── README.md                    # This file
```

## 🧠 Chatbot Capabilities

### Intent Recognition
The chatbot can understand and respond to:

- **Greetings**: "Hello", "Hi", "Hey"
- **Product Searches**: "I need...", "Show me...", "Find..."
- **Price Queries**: "Cheap", "Under $X", "Between $X and $Y"
- **Category Browsing**: "Electronics", "Fashion", "Home products"
- **Help Requests**: "Help", "What can you do?"
- **Farewells**: "Bye", "Thank you", "Goodbye"

### Search Features
- **Keyword Matching**: Searches product names and descriptions
- **Category Mapping**: Maps broad terms to specific categories
- **Price Filtering**: Finds products within specified price ranges
- **Stock Awareness**: Shows availability information
- **Rating Display**: Includes product ratings and reviews

### Response Generation
- **Contextual Responses**: Tailored based on user query type
- **Product Recommendations**: Shows relevant products with details
- **Formatted Output**: Clean, readable product information
- **Helpful Suggestions**: Guides users when searches return no results

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the Django project root:
```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### CORS Configuration
Frontend URLs are configured in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:5174'
]
```

## 🧪 Testing

### Run Backend Tests
```bash
cd firstproject
python manage.py test
```

### Run Frontend Tests
```bash
cd chatbot_frontend
npm test
```

### Manual Testing
1. Test user registration and login
2. Verify chat session creation
3. Test various chatbot queries
4. Check product search functionality
5. Validate API endpoints with Postman

## 🚀 Deployment

### Development
Both servers run locally:
- Django: http://localhost:8000
- React: http://localhost:5173

### Production Considerations
- Use PostgreSQL instead of SQLite
- Configure environment variables
- Set up HTTPS with SSL certificates
- Use a production WSGI server (Gunicorn)
- Implement caching with Redis
- Set up monitoring and logging

For detailed deployment instructions, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write tests for new features
- Update documentation for API changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter any issues or have questions:

1. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for common solutions
2. Review the [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for detailed information
3. Open an issue in the repository

## 🚀 Future Enhancements

- **Machine Learning Integration**: AI-powered product recommendations
- **Voice Interface**: Speech-to-text chatbot interaction
- **Real-time Features**: WebSocket-based live chat
- **Mobile App**: React Native version
- **Advanced Analytics**: User behavior tracking and insights
- **Multi-language Support**: Internationalization features

## 🙏 Acknowledgments

- [DummyJSON](https://dummyjson.com/) for providing realistic mock data
- [Django](https://www.djangoproject.com/) and [React](https://reactjs.org/) communities
- [TailwindCSS](https://tailwindcss.com/) for excellent styling utilities

---

**Built with ❤️ using Django and React** 