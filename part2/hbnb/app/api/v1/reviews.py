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

# Define a model for updating a review (only text and rating can be updated)
update_review_model = ns.model('UpdateReview', {
    'text': fields.String(required=False, description='Updated text of the review'),
    'rating': fields.Integer(required=False, description='Updated rating of the place (1-5)')
})

@ns.route('/')
class ReviewList(Resource):
    @ns.expect(review_model)  # Expect the review_model as input
    @ns.response(201, 'Review successfully created')
    @ns.response(400, 'Invalid input data')
    @ns.response(404, 'User or Place not found')
    def post(self):
        """
        Register a new review.
        
        Example payload:
        {
          "text": "Great place to stay!",
          "rating": 5,
          "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
        """
        review_data = ns.payload  # Get the JSON payload from the request

        try:
            # Use the facade to create the review
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
        except Exception as e:
            return {"error": "User or Place not found"}, 404

    @ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
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

    @ns.expect(update_review_model)
    @ns.response(200, 'Review updated successfully')
    @ns.response(404, 'Review not found')
    @ns.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        update_data = ns.payload
        try:
            updated_review = facade.update_review(review_id, update_data)
            if not updated_review:
                return {"error": "Review not found"}, 404

            return {"message": "Review updated successfully"}, 200
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
