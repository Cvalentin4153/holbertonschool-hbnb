from flask import Blueprint
from flask_restx import Api

# Create a Blueprint for API v1
v1_bp = Blueprint("v1", __name__, url_prefix="/api/v1")

# Initialize Flask-RESTX API
api = Api(
    v1_bp,
    version="1.0",
    title="HBnB API",
    description="API for the HBnB Evolution application",
    doc="/docs"
)

# Import namespaces (routes)
from app.api.v1.users import user_ns
from app.api.v1.amenities import amenity_ns
from app.api.v1.places import place_ns
from app.api.v1.reviews import review_ns
from app.api.v1.auth import api as auth_ns

# Add namespaces to API
api.add_namespace(user_ns, path="/users")
api.add_namespace(amenity_ns, path="/amenities")
api.add_namespace(place_ns, path="/places")
api.add_namespace(review_ns, path="/reviews")
api.add_namespace(auth_ns, path="/auth")
