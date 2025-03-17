from flask_restx import Namespace, Resource, fields
from app.services import facade

# Define the namespace
ns = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = ns.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@ns.route('')  # ✅ Corrected: This correctly maps to /api/v1/reviews
class ReviewList(Resource):
    @ns.expect(review_model)
    @ns.response(201, 'Review successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = ns.payload

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
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        } for review in reviews], 200


@ns.route('/<string:review_id>')  # ✅ Corrected to ensure proper route mapping
class ReviewResource(Resource):
    @ns.response(200, 'Review details retrieved successfully')
    @ns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
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

    @ns.expect(review_model)
    @ns.response(200, 'Review updated successfully')
    @ns.response(404, 'Review not found')
    @ns.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = ns.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {"error": "Review not found"}, 404

            return {
                "id": updated_review.id,
                "text": updated_review.text,
                "rating": updated_review.rating,
                "user_id": updated_review.user.id,
                "place_id": updated_review.place.id
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @ns.response(200, 'Review deleted successfully')
    @ns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200


@ns.route('/places/<string:place_id>')  # ✅ Corrected for valid route structure
class PlaceReviewList(Resource):
    @ns.response(200, 'List of reviews for the place retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {"error": "Place not found or no reviews available"}, 404

        return [{
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        } for review in reviews], 200
