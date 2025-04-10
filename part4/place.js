// part4/place.js

document.addEventListener('DOMContentLoaded', () => {
    console.log('[Place] DOMContentLoaded event fired');

    // Fetch and display place details on place.html
    const placeDetails = document.getElementById('place-details');
    console.log('[Place] placeDetails element:', placeDetails);

    if (!placeDetails) {
        console.error('[Place] place-details element not found');
        return;
    }

    // Get the placeId from the URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    console.log('[Place] URL search params:', urlParams.toString());

    let placeId = urlParams.get('placeId'); // Match the case used in places.js
    // Fallback for lowercase place_id in case of future changes
    if (!placeId) {
        placeId = urlParams.get('place_id');
        console.log('[Place] Fallback: Extracted place_id (lowercase):', placeId);
    }
    const errorMessageDiv = document.getElementById('error-message');
    console.log('[Place] URL:', window.location.href);
    console.log('[Place] Extracted placeId:', placeId);

    if (!errorMessageDiv) {
        console.error('[Place] error-message element not found');
        return;
    }

    if (!placeId) {
        console.log('[Place] No placeId found, exiting');
        errorMessageDiv.textContent = 'No place ID provided in the URL.';
        errorMessageDiv.style.display = 'block';
        return;
    }

    // Utility function to get cookie by name
    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        return null;
    };

    // Function to fetch user details by user_id
    const fetchUserDetails = async (userId) => {
        const token = getCookie('token');
        try {
            const response = await fetch(`http://localhost:5000/api/v1/users/${userId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : ''
                }
            });
            if (!response.ok) {
                throw new Error(`Failed to fetch user details for user_id: ${userId}, Status: ${response.status}`);
            }
            const userData = await response.json();
            return userData;
        } catch (error) {
            console.error('[Place] Error fetching user details:', error);
            return null;
        }
    };

    // Function to render reviews dynamically
    const renderReviews = async (reviews) => {
        const reviewsSection = document.getElementById('reviews');
        const reviewsContainer = reviewsSection.querySelector('h3').nextElementSibling || document.createElement('div');
        reviewsContainer.innerHTML = ''; // Clear existing reviews

        if (!reviews || reviews.length === 0) {
            reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
            reviewsSection.appendChild(reviewsContainer);
            return;
        }

        for (const review of reviews) {
            const reviewCard = document.createElement('div');
            reviewCard.classList.add('review-card');
            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);

            // Fetch user details for the reviewer
            const user = await fetchUserDetails(review.user_id);
            const reviewerName = user && user.first_name && user.last_name 
                ? `${user.first_name} ${user.last_name}`
                : `User ID: ${review.user_id}`;

            reviewCard.innerHTML = `
                <p><strong>${reviewerName}</strong></p>
                <p>${review.text}</p>
                <p><strong>Rating:</strong> ${stars}</p>
            `;
            reviewsContainer.appendChild(reviewCard);
        }
        reviewsSection.appendChild(reviewsContainer);
    };

    // Function to fetch place details (including reviews)
    const fetchPlaceDetails = () => {
        const apiUrl = `http://localhost:5000/api/v1/places/${placeId}`;
        console.log('[Place] Fetching place details from:', apiUrl);

        return fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log('[Place] Fetch response status:', response.status);
            console.log('[Place] Fetch response headers:', response.headers.get('Content-Type'));
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('Place not found. The place ID may be invalid.');
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const contentType = response.headers.get('Content-Type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Invalid response: Expected JSON, but received HTML or another format.');
            }
            return response.json();
        });
    };

    // Initial fetch of place details
    fetchPlaceDetails()
    .then(data => {
        console.log('[Place] Fetched place data:', data);
        // Populate the place details
        document.getElementById('place-name').textContent = data.title || 'No title provided';
        document.getElementById('place-host').textContent = data.owner && data.owner.first_name && data.owner.last_name 
            ? `${data.owner.first_name} ${data.owner.last_name}` 
            : data.owner && data.owner.id 
            ? data.owner.id 
            : 'Unknown host';
        document.getElementById('place-price').textContent = data.price || 'N/A';
        document.getElementById('place-description').textContent = data.description || 'No description provided';
        const amenities = Array.isArray(data.amenities) && data.amenities.length > 0 
            ? data.amenities.map(amenity => typeof amenity === 'object' && amenity.name ? amenity.name : amenity).join(', ')
            : 'None';
        document.getElementById('place-amenities').textContent = amenities;

        // Render the reviews
        renderReviews(data.reviews);
    })
    .catch(error => {
        console.error('[Place] Error fetching place details:', error);
        errorMessageDiv.textContent = error.message || 'An error occurred while fetching place details. Please ensure the backend server is running.';
        errorMessageDiv.style.display = 'block';
    });

    // Handle review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value;
            const rating = parseInt(document.getElementById('rating').value);
            const token = getCookie('token');

            if (!token) {
                errorMessageDiv.textContent = 'You must be logged in to submit a review.';
                errorMessageDiv.style.display = 'block';
                return;
            }

            const reviewData = {
                text: reviewText,
                rating: rating,
                place_id: placeId
            };

            fetch('http://localhost:5000/api/v1/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(reviewData)
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Unauthorized: Please log in again.');
                    }
                    if (response.status === 400) {
                        return response.json().then(data => {
                            throw new Error(data.error || 'Invalid review data. Please check your input.');
                        });
                    }
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('[Place] Review submitted:', data);
                // Clear the form
                reviewForm.reset();
                // Refetch place details to update the reviews list
                return fetchPlaceDetails();
            })
            .then(data => {
                // Re-render the reviews
                renderReviews(data.reviews);
            })
            .catch(error => {
                console.error('[Place] Error submitting review:', error);
                errorMessageDiv.textContent = error.message || 'An error occurred while submitting your review.';
                errorMessageDiv.style.display = 'block';
            });
        });
    }
});