from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

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
    "owner_id": fields.String(required=True, description="ID of the owner"),
    "amenities": fields.List(fields.String, required=False, description="List of Amenity IDs"),
    "reviews": fields.List(fields.String, description="List of review IDs")
})

@place_ns.route("/")
class PlaceList(Resource):
    @place_ns.expect(place_model, validate=True)
    @place_ns.response(201, "Place successfully created")
    @place_ns.response(400, "Invalid input data")
    def post(self):
        """Register a new place."""
        data = request.json
        try:
            new_place = facade.create_place(
                title=data["title"],
                description=data.get("description", ""),
                price=data["price"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                owner_id=data["owner_id"],
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
            return {"error": str(e)}, 400

    @place_ns.response(200, "List of places retrieved successfully")
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
            ]
        }, 200

    @place_ns.expect(place_model, validate=True)
    @place_ns.response(200, "Place updated successfully")
    @place_ns.response(404, "Place not found")
    @place_ns.response(400, "Invalid input data")
    def put(self, place_id):
        """Update a place's information."""
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
