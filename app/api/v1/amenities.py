from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

amenity_ns = Namespace('amenities', description='Amenity operations')

amenity_model = amenity_ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@amenity_ns.route('/')
class AmenityList(Resource):
    @jwt_required()
    @amenity_ns.expect(amenity_model, validate=True)
    @amenity_ns.response(201, 'Amenity successfully created')
    @amenity_ns.response(400, 'Invalid input data')
    @amenity_ns.response(403, 'Unauthorized action')
    def post(self):
        """Create a new amenity. Admin only."""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Only administrators can create amenities'}, 403

        data = request.json
        try:
            new_amenity = facade.create_amenity(data['name'])
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @amenity_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities. Public endpoint."""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ], 200

@amenity_ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @amenity_ns.response(200, 'Amenity details retrieved successfully')
    @amenity_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details. Public endpoint."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @jwt_required()
    @amenity_ns.expect(amenity_model, validate=True)
    @amenity_ns.response(200, 'Amenity updated successfully')
    @amenity_ns.response(404, 'Amenity not found')
    @amenity_ns.response(400, 'Invalid input data')
    @amenity_ns.response(403, 'Unauthorized action')
    def put(self, amenity_id):
        """Update an amenity. Admin only."""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Only administrators can modify amenities'}, 403

        data = request.json
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404
