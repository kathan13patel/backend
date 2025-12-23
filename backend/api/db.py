# backend/api/db.py
from pymongo import MongoClient
from django.conf import settings
import certifi
import ssl

def get_mongodb_connection():
    """
    Establish connection to MongoDB Atlas
    """
    try:
        # For MongoDB Atlas with SSL
        client = MongoClient(
            settings.MONGODB_URI,
            tls=True,
            tlsCAFile=certifi.where(),
            retryWrites=True,
            w='majority'
        )
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        return client[settings.MONGODB_DB_NAME]
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise

# Initialize database connection
try:
    db = get_mongodb_connection()
except Exception as e:
    print(f"Failed to initialize MongoDB connection: {e}")
    db = None