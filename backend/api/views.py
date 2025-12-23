# backend/api/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserRegistration
import re

@csrf_exempt
def register_user(request):
    """Handle user registration"""
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body.decode('utf-8'))
            
            # Required fields validation
            required_fields = ['name', 'email', 'phone', 'age']
            missing_fields = []
            
            for field in required_fields:
                if field not in data or not data[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                return JsonResponse({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }, status=400)
            
            # Email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data['email']):
                return JsonResponse({
                    'error': 'Invalid email format'
                }, status=400)
            
            # Phone validation (basic)
            phone_pattern = r'^\+?[1-9]\d{1,14}$'
            if not re.match(phone_pattern, str(data['phone'])):
                return JsonResponse({
                    'error': 'Invalid phone number format'
                }, status=400)
            
            # Age validation
            try:
                age = int(data['age'])
                if age < 1 or age > 120:
                    return JsonResponse({
                        'error': 'Age must be between 1 and 120'
                    }, status=400)
                data['age'] = age
            except ValueError:
                return JsonResponse({
                    'error': 'Age must be a number'
                }, status=400)
            
            # Create user in MongoDB
            user = UserRegistration.create_user(data)
            
            return JsonResponse({
                'message': 'Registration successful!',
                'user': {
                    'name': user['name'],
                    'email': user['email'],
                    'id': user['_id']
                }
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # Check if it's a duplicate email error
            if "duplicate key error" in str(e):
                return JsonResponse({
                    'error': 'Email already registered'
                }, status=409)
            return JsonResponse({
                'error': f'Registration failed: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_all_users(request):
    """Get all registered users"""
    if request.method == 'GET':
        try:
            users = UserRegistration.get_all_users()
            
            # Remove MongoDB _id and timestamps from response if not needed
            for user in users:
                user.pop('_id', None)
                user.pop('created_at', None)
                user.pop('updated_at', None)
            
            return JsonResponse({
                'users': users,
                'count': len(users)
            }, safe=False)
            
        except Exception as e:
            return JsonResponse({
                'error': f'Failed to fetch users: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_users_count(request):
    """Get total number of registrations"""
    if request.method == 'GET':
        try:
            count = UserRegistration.get_users_count()
            return JsonResponse({
                'total_registrations': count,
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Failed to get count: {str(e)}',
                'status': 'error'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)