from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

user_ns = Namespace("users", description="User management endpoints")

user_model = user_ns.model("User", {
    "first_name": fields.String(required=True, description="First name of the user"),
    "last_name": fields.String(required=True, description="Last name of the user"),
    "email": fields.String(required=True, description="Email of the user"),
    "password": fields.String(required=True, description="Password of the user")
})

user_update_model = user_ns.model("UserUpdate", {
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name")
})

@user_ns.route("/")
class UserList(Resource):
    @user_ns.expect(user_model, validate=True)
    @user_ns.response(201, "User successfully created")
    @user_ns.response(400, "Email already registered")
    @user_ns.response(400, "Invalid input data")
    def post(self):
        user_data = request.json

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400
        try:
            new_user = facade.create_user(**user_data)
            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            }, 201
        except TypeError as e:
            return {"error": str(e)}, 400
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @user_ns.response(200, "Users retrieved successfully")
    def get(self):
        users = facade.get_all_users()
        return [{
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        } for user in users], 200

@user_ns.route("/<string:user_id>")
class UserResource(Resource):
    @jwt_required()
    @user_ns.response(200, "User details retrieved successfully")
    @user_ns.response(404, "User not found")
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 200

    @jwt_required()
    @user_ns.expect(user_update_model, validate=True)
    @user_ns.response(200, "User updated successfully")
    @user_ns.response(404, "User not found")
    @user_ns.response(400, "Invalid input data")
    @user_ns.response(403, "Unauthorized action")
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        if user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
            
        data = request.json
        if "email" in data or "password" in data:
            return {"error": "You cannot modify email or password"}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            return {
                "id": updated_user.id,
                "first_name": updated_user.first_name,
                "last_name": updated_user.last_name,
                "email": updated_user.email
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
        current_user_id = get_jwt_identity()
        user = facade.get_user(current_user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
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
