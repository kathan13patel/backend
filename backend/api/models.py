# backend/api/models.py
from datetime import datetime
from .db import db

class UserRegistration:
    """MongoDB operations for user registration"""
    
    @staticmethod
    def get_collection():
        """Get users collection"""
        if db is None:
            raise Exception("Database connection not initialized")
        return db['users']
    
    @staticmethod
    def create_user(user_data):
        """Create a new user document"""
        try:
            collection = UserRegistration.get_collection()
            
            # Add timestamps
            user_data['created_at'] = datetime.utcnow()
            user_data['updated_at'] = datetime.utcnow()
            
            # Insert document
            result = collection.insert_one(user_data)
            
            # Return the inserted document with string ID
            inserted_doc = collection.find_one({"_id": result.inserted_id})
            inserted_doc['_id'] = str(inserted_doc['_id'])
            return inserted_doc
            
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
    
    @staticmethod
    def get_all_users():
        """Get all users from the collection"""
        try:
            collection = UserRegistration.get_collection()
            
            # Get all users, convert ObjectId to string
            users = list(collection.find({}))
            
            # Convert ObjectId to string for JSON serialization
            for user in users:
                user['_id'] = str(user['_id'])
                # Convert datetime to string if needed
                if 'created_at' in user:
                    user['created_at'] = user['created_at'].isoformat()
                if 'updated_at' in user:
                    user['updated_at'] = user['updated_at'].isoformat()
            
            return users
            
        except Exception as e:
            print(f"Error getting users: {e}")
            raise
    
    @staticmethod
    def get_users_count():
        """Get total number of registered users"""
        try:
            collection = UserRegistration.get_collection()
            return collection.count_documents({})
        except Exception as e:
            print(f"Error getting user count: {e}")
            raise
    
    @staticmethod
    def create_indexes():
        """Create indexes for better performance"""
        try:
            collection = UserRegistration.get_collection()
            
            # Create unique index on email
            collection.create_index([("email", 1)], unique=True)
            
            # Create index on name for faster searches
            collection.create_index([("name", 1)])
            
            print("✅ Database indexes created successfully")
            
        except Exception as e:
            print(f"Note: Index creation failed (might already exist): {e}")