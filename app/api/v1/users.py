from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

user_ns = Namespace("users", description="User management endpoints")

user_model = user_ns.model("User", {
    "first_name": fields.String(required=True, description="First name of the user"),
    "last_name": fields.String(required=True, description="Last name of the user"),
    "email": fields.String(required=True, description="Email of the user"),
    "password": fields.String(required=True, description="Password of the user"),
    "is_admin": fields.Boolean(description="Admin status of the user", default=False)
})

user_update_model = user_ns.model("UserUpdate", {
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name"),
    "email": fields.String(description="Email"),
    "password": fields.String(description="Password"),
    "is_admin": fields.Boolean(description="Admin status")
})

@user_ns.route("/")
class UserList(Resource):
    @user_ns.expect(user_model, validate=True)
    @user_ns.response(201, "User successfully created")
    @user_ns.response(400, "Email already registered")
    @user_ns.response(400, "Invalid input data")
    @jwt_required(optional=True)
    def post(self):
        """Create a new user. Only admins can create admin users."""
        user_data = request.json
        current_user = get_jwt_identity()

        # If is_admin is True in request, ensure current user is admin
        if user_data.get('is_admin', False):
            if not current_user or not current_user.get('is_admin', False):
                return {"error": "Only administrators can create admin users"}, 403

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400
        try:
            new_user = facade.create_user(**user_data)
            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "is_admin": new_user.is_admin
            }, 201
        except TypeError as e:
            return {"error": str(e)}, 400
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @user_ns.response(200, "Users retrieved successfully")
    def get(self):
        """Get all users. Regular users can only see basic info."""
        current_user = get_jwt_identity()
        users = facade.get_all_users()
        
        # If admin, return full user details
        if current_user.get('is_admin', False):
            return [{
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_admin": user.is_admin
            } for user in users], 200
        
        # For regular users, return limited info
        return [{
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name
        } for user in users], 200

@user_ns.route("/<string:user_id>")
class UserResource(Resource):
    @jwt_required()
    @user_ns.response(200, "User details retrieved successfully")
    @user_ns.response(404, "User not found")
    def get(self, user_id):
        """Get user details. Regular users can only see their own full details."""
        current_user = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
            
        # If admin or own profile, return full details
        if current_user.get('is_admin', False) or current_user.get('id') == user_id:
            return {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_admin": user.is_admin
            }, 200
            
        # For other users, return limited info
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name
        }, 200

    @jwt_required()
    @user_ns.expect(user_update_model, validate=True)
    @user_ns.response(200, "User updated successfully")
    @user_ns.response(404, "User not found")
    @user_ns.response(400, "Invalid input data")
    @user_ns.response(403, "Unauthorized action")
    def put(self, user_id):
        """Update user details. Admins can update any user, regular users can only update themselves."""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
            
        # Only admins can modify other users
        if not is_admin and current_user.get('id') != user_id:
            return {"error": "Unauthorized action"}, 403
            
        data = request.json
        
        # Only admins can modify admin status
        if 'is_admin' in data and not is_admin:
            return {"error": "Only administrators can modify admin status"}, 403
            
        # Regular users cannot modify their email or password
        if not is_admin and (data.get('email') or data.get('password')):
            return {"error": "Only administrators can modify email or password"}, 403

        try:
            updated_user = facade.update_user(user_id, data)
            return {
                "id": updated_user.id,
                "first_name": updated_user.first_name,
                "last_name": updated_user.last_name,
                "email": updated_user.email,
                "is_admin": updated_user.is_admin
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 404

@user_ns.route("/me")
class CurrentUser(Resource):
    @jwt_required()
    @user_ns.response(200, "Current user details retrieved successfully")
    @user_ns.response(404, "User not found")
    def get(self):
        """Get current user's profile."""
        current_user = get_jwt_identity()
        user = facade.get_user(current_user.get('id'))
        if not user:
            return {"error": "User not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin
        }, 200

@user_ns.route("/<string:user_id>/places")
class UserPlacesResource(Resource):
    @jwt_required()
    @user_ns.response(200, "User's places retrieved successfully")
    @user_ns.response(404, "User not found")
    @user_ns.response(403, "Unauthorized action")
    def get(self, user_id):
        """Get all places owned by a user."""
        current_user_id = get_jwt_identity()
        if user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
            
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
            
        places = [{
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "amenities": [{"id": a.id, "name": a.name} for a in place.amenities],
            "reviews": [{"id": r.id, "text": r.text, "rating": r.rating} for r in place.reviews]
        } for place in user.places]
        
        return places, 200
