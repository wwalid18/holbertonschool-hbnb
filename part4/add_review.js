// part4/add_review.js

document.addEventListener('DOMContentLoaded', () => {
    console.log('[AddReview] DOMContentLoaded event fired');

    // Utility function to get cookie by name
    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        return null;
    };

    // Check user authentication
    const checkAuthentication = () => {
        const token = getCookie('token');
        if (!token) {
            console.log('[AddReview] No token found, redirecting to index.html');
            // Store an error message in localStorage to display on index.html
            localStorage.setItem('errorMessage', 'You must be logged in to add a review.');
            window.location.href = 'index.html';
        }
        return token;
    };

    // Get place ID from URL
    const getPlaceIdFromURL = () => {
        const urlParams = new URLSearchParams(window.location.search);
        let placeId = urlParams.get('placeId'); // Match the case used in other pages
        // Fallback for lowercase place_id
        if (!placeId) {
            placeId = urlParams.get('place_id');
            console.log('[AddReview] Fallback: Extracted place_id (lowercase):', placeId);
        }
        console.log('[AddReview] Extracted placeId:', placeId);
        return placeId;
    };

    // Function to display messages
    const displayMessage = (message, isError = false) => {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = message;
        messageDiv.style.color = isError ? 'red' : 'green';
        messageDiv.style.display = 'block';
        // Hide the message after 5 seconds (only for errors, since success will redirect)
        if (isError) {
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    };

    // Check authentication and get place ID
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        console.log('[AddReview] No placeId found in URL');
        displayMessage('No place ID provided in the URL.', true);
        return;
    }

    // Setup event listener for review form
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('[AddReview] Review form submitted');

            const reviewText = document.getElementById('review-text').value;
            const rating = parseInt(document.getElementById('rating').value);

            // Validate input
            if (!reviewText || isNaN(rating)) {
                displayMessage('Please provide a review and a rating.', true);
                return;
            }

            const reviewData = {
                text: reviewText,
                rating: rating,
                place_id: placeId
            };

            console.log('[AddReview] Submitting review data:', reviewData);

            // Make AJAX request to submit review
            try {
                const response = await fetch('http://localhost:5000/api/v1/reviews/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(reviewData)
                });

                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Unauthorized: Please log in again.');
                    }
                    if (response.status === 400) {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Invalid review data. Please check your input.');
                    }
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                console.log('[AddReview] Review submitted successfully:', data);

                // Display success message briefly before redirecting
                displayMessage('Review submitted successfully!');
                // Redirect to the place.html page for the reviewed place after a short delay
                setTimeout(() => {
                    window.location.href = `place.html?placeId=${placeId}`;
                }, 2000); // 2-second delay to allow the user to see the success message
            } catch (error) {
                console.error('[AddReview] Error submitting review:', error);
                displayMessage(error.message || 'An error occurred while submitting your review.', true);
            }
        });
    }
});