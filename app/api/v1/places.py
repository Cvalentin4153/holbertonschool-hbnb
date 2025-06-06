from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_cors import cross_origin
from flask import current_app

place_ns = Namespace("places", description="Place operations")

# Models for related entities
amenity_model = place_ns.model("PlaceAmenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Name of the amenity")
})

user_model = place_ns.model("PlaceUser", {
    "id": fields.String(description="User ID"),
    "first_name": fields.String(description="First name of the owner"),
    "last_name": fields.String(description="Last name of the owner"),
    "email": fields.String(description="Email of the owner")
})

place_model = place_ns.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "amenities": fields.List(fields.String, required=False, description="List of Amenity IDs"),
    "reviews": fields.List(fields.String, description="List of review IDs")
})

place_update_model = place_ns.model("PlaceUpdate", {
    "title": fields.String(description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(description="Price per night"),
    "latitude": fields.Float(description="Latitude of the place"),
    "longitude": fields.Float(description="Longitude of the place"),
    "amenities": fields.List(fields.String, description="List of Amenity IDs")
})


@place_ns.route("/")
class PlaceList(Resource):
    @jwt_required()
    @place_ns.expect(place_model, validate=True)
    @place_ns.response(201, "Place successfully created")
    @place_ns.response(400, "Invalid input data")
    @cross_origin()
    def post(self):
        """Register a new place."""
        data = request.json
        current_user_id = get_jwt_identity()  # This will now be the string user ID
        
        # Log the current user ID for debugging
        current_app.logger.debug(f"User ID from token: {current_user_id}")
        
        if not current_user_id:
            return {"error": "User ID not found in token"}, 401
            
        try:
            # Log the data being sent to create_place
            current_app.logger.debug(f"Creating place with data: {data}")
            current_app.logger.debug(f"Owner ID: {current_user_id}")
            
            new_place = facade.create_place(
                title=data["title"],
                description=data.get("description", ""),
                price=data["price"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                owner_id=current_user_id,
                amenities=data.get("amenities", [])
            )
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner.id,
                "amenities": [a.id for a in new_place.amenities]
            }, 201
        except ValueError as e:
            current_app.logger.error(f"ValueError in create_place: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            import traceback
            current_app.logger.error(f"Error creating place: {str(e)}")
            current_app.logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}", "traceback": traceback.format_exc()}, 500

    @place_ns.response(200, "List of places retrieved successfully")
    @cross_origin()
    def get(self):
        """Retrieve a list of all places."""
        places = facade.get_all_places()
        results = []
        for p in places:
            results.append({
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner.id,
                "amenities": [a.id for a in p.amenities],
                "reviews": [r.id for r in p.reviews]
            })
        return results, 200

@place_ns.route("/<string:place_id>")
class PlaceResource(Resource):
    @place_ns.response(200, "Place details retrieved successfully")
    @place_ns.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID, including owner and amenities."""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Build the place's JSON, including owner and amenities
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email
            },
            "amenities": [
                {"id": a.id, "name": a.name} for a in place.amenities
            ],
            "reviews": [
                {"id": r.id, "text": r.text, "rating": r.rating, "user_id": r.user_id} for r in place.reviews
            ]
        }, 200

    @jwt_required()
    @place_ns.expect(place_update_model, validate=True)
    @place_ns.response(200, "Place updated successfully")
    @place_ns.response(404, "Place not found")
    @place_ns.response(400, "Invalid input data")
    @place_ns.response(403, "Unauthorized action")
    def put(self, place_id):
        """Update a place's information. Admins can update any place."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
            
        # Allow admins to bypass ownership check
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
            
        data = request.json
        try:
            updated_place = facade.update_place(place_id, data)
            return {
                "id": updated_place.id,
                "title": updated_place.title,
                "description": updated_place.description,
                "price": updated_place.price,
                "latitude": updated_place.latitude,
                "longitude": updated_place.longitude,
                "owner_id": updated_place.owner.id,
                "amenities": [a.id for a in updated_place.amenities]
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 404

@place_ns.route("/<string:place_id>/amenities/<string:amenity_id>")
class PlaceAmenityResource(Resource):
    @jwt_required()
    @place_ns.response(200, "Amenity linked to place successfully")
    @place_ns.response(404, "Place or amenity not found")
    @place_ns.response(403, "Unauthorized action")
    def post(self, place_id, amenity_id):
        """Link an amenity to a place. Admins can link amenities to any place."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
            
        # Allow admins to bypass ownership check
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403
            
        try:
            facade.link_amenity_to_place(place_id, amenity_id)
            return {"message": "Amenity linked successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
