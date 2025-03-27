# app/api/v1/reviews.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

ns = Namespace('reviews', description='Review operations')

# Model for creating a review.
review_model = ns.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
    # user_id is not included; it will be set from the JWT.
})

# Model for updating a review (only text and rating can be updated)
update_review_model = ns.model('UpdateReview', {
    'text': fields.String(required=False, description='Updated text of the review'),
    'rating': fields.Integer(required=False, description='Updated rating of the place (1-5)')
})

@ns.route('/')
class ReviewList(Resource):
    @jwt_required()
    @ns.expect(review_model, validate=True)
    @ns.response(201, 'Review successfully created')
    @ns.response(400, 'Invalid input data or review not allowed')
    def post(self):
        """Create a new review (protected)
        
        Validation Rules:
          - The user must be authenticated.
          - The place_id must belong to an existing place.
          - The authenticated user must not be the owner of the place.
          - The user can only review a place once.
        """
        current_user = get_jwt_identity()  # Retrieve authenticated user's identity
        review_data = ns.payload
        
        # Override user_id with the authenticated user's id
        review_data['user_id'] = current_user['id']
        
        # Retrieve the place details to ensure it exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Prevent self-review: the user must not be the owner of the place.
        if place.get('owner', {}).get('id') == current_user['id']:
            return {'error': 'You cannot review your own place.'}, 400
        
        # Prevent duplicate reviews: ensure the user hasn't already reviewed this place.
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for review in existing_reviews:
            if review.user.id == current_user['id']:
                return {'error': 'You have already reviewed this place.'}, 400
        
        try:
            new_review = facade.create_review(review_data)
            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user.id,
                "place_id": new_review.place.id
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews (public endpoint)"""
        reviews = facade.get_all_reviews()
        return [{
            "id": review.id,
            "text": review.text,
            "rating": review.rating
        } for review in reviews], 200

@ns.route('/<string:review_id>')
class ReviewResource(Resource):
    @ns.response(200, 'Review details retrieved successfully')
    @ns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (public endpoint)"""
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
    @ns.expect(update_review_model, validate=True)
    @ns.response(200, 'Review updated successfully')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (protected: only the creator can update)
        
        Ensures that the authenticated user is the creator of the review.
        """
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if review.user.id != current_user['id']:
            return {"error": "Unauthorized action"}, 403
        update_data = ns.payload
        try:
            updated_review = facade.update_review(review_id, update_data)
            return {"message": "Review updated successfully", "review": {
                "id": updated_review.id,
                "text": updated_review.text,
                "rating": updated_review.rating,
                "user_id": updated_review.user.id,
                "place_id": updated_review.place.id
            }}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @ns.response(200, 'Review deleted successfully')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (protected: only the creator can delete)
        
        Ensures that the authenticated user is the creator of the review.
        """
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if review.user.id != current_user['id']:
            return {"error": "Unauthorized action"}, 403
        deletion_result = facade.delete_review(review_id)
        if deletion_result:
            return {"message": "Review deleted successfully"}, 200
        else:
            return {"error": "Failed to delete review"}, 400
