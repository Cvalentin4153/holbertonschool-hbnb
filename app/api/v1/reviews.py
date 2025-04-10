from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

review_ns = Namespace("reviews", description="Review operations")

review_model = review_ns.model("Review", {
    "text": fields.String(required=True, description="Review text"),
    "rating": fields.Integer(required=True, description="Rating (1-5)"),
    "place_id": fields.String(required=True, description="ID of the place being reviewed")
})

review_update_model = review_ns.model("ReviewUpdate", {
    "text": fields.String(description="Review text"),
    "rating": fields.Integer(description="Rating (1-5)")
})

@review_ns.route("/")
class ReviewList(Resource):
    @jwt_required()
    @review_ns.expect(review_model)
    @review_ns.response(201, "Review successfully created")
    @review_ns.response(400, "Invalid input data")
    @review_ns.response(403, "Unauthorized action")
    def post(self):
        """Register a new review."""
        data = request.json
        current_user_id = get_jwt_identity()
        
        # Check if user owns the place
        place = facade.get_place(data["place_id"])
        if not place:
            return {"error": "Place not found"}, 404
            
        if place.owner_id == current_user_id:
            return {"error": "You cannot review your own place"}, 403
            
        # Check if user has already reviewed this place
        existing_reviews = facade.get_reviews_by_place(data["place_id"])
        for review in existing_reviews:
            if review.user_id == current_user_id:
                return {"error": "You have already reviewed this place"}, 400
        
        try:
            new_review = facade.create_review(
                text=data["text"],
                rating=data["rating"],
                user_id=current_user_id,
                place_id=data["place_id"]
            )
            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user.id,
                "place_id": new_review.place.id
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @review_ns.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve a list of all reviews."""
        reviews = facade.get_all_reviews()
        results = []
        for r in reviews:
            results.append({
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id,
                "place_id": r.place.id
            })
        return results, 200

@review_ns.route("/<string:review_id>")
class ReviewResource(Resource):
    @review_ns.response(200, "Review details retrieved successfully")
    @review_ns.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 200

    @jwt_required()
    @review_ns.expect(review_update_model, validate=True)
    @review_ns.response(200, "Review updated successfully")
    @review_ns.response(404, "Review not found")
    @review_ns.response(400, "Invalid input data")
    @review_ns.response(403, "Unauthorized action")
    def put(self, review_id):
        """Update a review's information. Admins can update any review."""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
            
        # Allow admins to bypass ownership check
        if not is_admin and review.user_id != current_user.get('id'):
            return {"error": "Unauthorized action"}, 403
            
        data = request.json
        try:
            updated = facade.update_review(review_id, data)
            return {
                "id": updated.id,
                "text": updated.text,
                "rating": updated.rating,
                "user_id": updated.user.id,
                "place_id": updated.place.id
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 404

    @jwt_required()
    @review_ns.response(200, "Review deleted successfully")
    @review_ns.response(404, "Review not found")
    @review_ns.response(403, "Unauthorized action")
    def delete(self, review_id):
        """Delete a review. Admins can delete any review."""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
            
        # Allow admins to bypass ownership check
        if not is_admin and review.user_id != current_user.get('id'):
            return {"error": "Unauthorized action"}, 403
            
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404

@review_ns.route("/places/<string:place_id>/reviews")
class PlaceReviewList(Resource):
    @review_ns.response(200, "List of reviews for the place retrieved successfully")
    @review_ns.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place."""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            results = []
            for r in reviews:
                results.append({
                    "id": r.id,
                    "text": r.text,
                    "rating": r.rating,
                    "user_id": r.user.id
                })
            return results, 200
        except ValueError as e:
            return {"error": str(e)}, 404
