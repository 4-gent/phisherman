# Backend Configuration Guide

This document explains how to configure the Phisherman backend.

## 📁 **Configuration Structure**

The backend now uses a centralized configuration system:

- **`config.py`** - Main configuration file with all settings
- **`connect.py`** - MongoDB connection using config
- **`routes/routes.py`** - Flask routes using config
- **`main.py`** - Server startup using config

## 🔧 **Configuration Options**

### **MongoDB Settings**
```python
MONGO_URI = "mongodb+srv://dsoc:dsoc@cluster0.dplte2b.mongodb.net/?appName=Cluster0"
DATABASE_NAME = "phish"
```

### **Flask Settings**
```python
SECRET_KEY = "im-phishing-it"
FLASK_ENV = "development"
FLASK_DEBUG = True
```

### **Server Settings**
```python
HOST = "0.0.0.0"
PORT = 8080
```

### **CORS Settings**
```python
CORS_ORIGINS = ["http://localhost:3000"]
```

### **Agent Settings**
```python
AGENT_PORTS = {
    'phish_master': 8001,
    'finance_phisher': 8002,
    'health_phisher': 8003,
    'personal_phisher': 8004,
    'phish_refiner': 8005
}
```

## 🌍 **Environment Variables**

You can override any configuration by setting environment variables:

```bash
# MongoDB
export MONGO_URI="your-mongodb-uri"
export DATABASE_NAME="your-database-name"

# Flask
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"
export FLASK_DEBUG="False"

# Server
export HOST="0.0.0.0"
export PORT="8080"

# CORS
export CORS_ORIGINS="http://localhost:3000,https://yourdomain.com"
```

## 🚀 **Usage Examples**

### **Development Mode**
```python
from config import config

# Check if in development
if config.is_development():
    print("Running in development mode")

# Get MongoDB URI
mongo_uri = config.get_mongo_uri()

# Get agent port
port = config.get_agent_port('phish_master')  # Returns 8001
```

### **Production Mode**
```bash
export FLASK_ENV="production"
export FLASK_DEBUG="False"
export SESSION_COOKIE_SECURE="True"
```

## 📝 **Configuration Benefits**

✅ **Centralized**: All settings in one place
✅ **Environment-aware**: Different configs for dev/prod
✅ **Type-safe**: Proper data types and validation
✅ **Flexible**: Easy to override with environment variables
✅ **Maintainable**: Clear structure and documentation

## 🔒 **Security Notes**

- **Never commit** `.env` files to version control
- **Use strong secrets** in production
- **Enable HTTPS** in production (`SESSION_COOKIE_SECURE=True`)
- **Restrict CORS origins** in production

## 🎯 **Quick Start**

1. **Default configuration** works out of the box
2. **MongoDB URI** is already configured
3. **All agents** have proper port assignments
4. **CORS** is configured for frontend communication

## 📚 **File Structure**

```
backend/
├── config.py              # Main configuration
├── connect.py             # MongoDB connection
├── main.py                # Server startup
├── routes/
│   └── routes.py          # Flask routes
└── mail/sender/           # Agent configurations
    ├── phish_master/
    ├── finance_phisher/
    ├── health_phisher/
    ├── personal_phisher/
    └── phish_refiner/
```

## 🚀 **Next Steps**

1. **Test the configuration**: `python main.py`
2. **Start agents**: Use the configured ports
3. **Register on Agentverse**: Use agent configurations
4. **Deploy to production**: Set production environment variables
