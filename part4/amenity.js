// amenity.js
document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------
    // Utility Function: Get Cookie by Name
    // -------------------------------------
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) {
        return parts.pop().split(';').shift();
      }
      return null;
    };
  
    // -------------------------------------
    // Extract Place ID from URL Query Parameters
    // -------------------------------------
    const urlParams = new URLSearchParams(window.location.search);
    let placeId = urlParams.get('placeId');
    if (!placeId) {
      // Fallback in case it is provided as "place_id" in lowercase.
      placeId = urlParams.get('place_id');
    }
    console.log('[Amenity] Place ID:', placeId);
    if (!placeId) {
      console.error('[Amenity] No place ID found in the URL.');
      return;
    }
  
    // -------------------------------------
    // Get JWT Token from Cookies
    // -------------------------------------
    const token = getCookie('token');
    if (!token) {
      console.error('[Amenity] User is not authenticated.');
      return;
    }
  
    // -------------------------------------
    // Toggle the "Add Amenity" Form
    // -------------------------------------
    const toggleAmenityBtn = document.getElementById('toggle-amenity-form');
    const amenityFormContainer = document.getElementById('add-amenity');
    if (toggleAmenityBtn && amenityFormContainer) {
      toggleAmenityBtn.addEventListener('click', () => {
        // Toggle the display between none and block.
        if (amenityFormContainer.style.display === 'none' || amenityFormContainer.style.display === '') {
          amenityFormContainer.style.display = 'block';
        } else {
          amenityFormContainer.style.display = 'none';
        }
      });
    }
  
    // -------------------------------------
    // Setup Event Listener for Amenity Form Submission
    // -------------------------------------
    const amenityForm = document.getElementById('amenity-form');
    // We'll use the error-message element to display messages.
    const errorMessageDiv = document.getElementById('error-message');
  
    if (amenityForm) {
      amenityForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission behavior
  
        // Get the amenity name entered by the user.
        const amenityNameInput = document.getElementById('amenity-name');
        if (!amenityNameInput) return;
        const amenityName = amenityNameInput.value.trim();
        console.log('[Amenity] Submitting amenity:', amenityName);
  
        // -- Duplicate Check on the Front End --
        // Get the current amenity list text from the place-amenities element.
        const amenitiesElement = document.getElementById('place-amenities');
        if (amenitiesElement) {
          // Assuming the amenities are displayed as a comma-separated list.
          const currentAmenities = amenitiesElement.innerText;
          // If the text is still "Loading...", we don't perform the check.
          if (currentAmenities.toLowerCase() !== 'loading...') {
            // Create an array of amenity names in lower-case, trimming whitespace.
            const amenityArray = currentAmenities.split(',').map(item => item.trim().toLowerCase());
            // Check if the amenity name is already in the array.
            if (amenityArray.includes(amenityName.toLowerCase())) {
              if (errorMessageDiv) {
                errorMessageDiv.textContent = 'This amenity has already been added.';
                errorMessageDiv.style.color = 'red';
                errorMessageDiv.style.display = 'block';
                setTimeout(() => {
                  errorMessageDiv.style.display = 'none';
                }, 3000);
              }
              return; // Stop processing if duplicate is found.
            }
          }
        }
  
        // Prepare the payload with amenity name and place ID.
        const amenityData = {
          name: amenityName,
          place_id: placeId
        };
  
        // Make AJAX POST request to submit the amenity.
        fetch('http://localhost:5000/api/v1/amenities/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(amenityData)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Failed to add amenity. Status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log('[Amenity] Amenity added successfully:', data);
          // Instead of an alert, show a success message.
          if (errorMessageDiv) {
            errorMessageDiv.textContent = 'Amenity added successfully!';
            errorMessageDiv.style.color = 'green';
            errorMessageDiv.style.display = 'block';
            setTimeout(() => {
              errorMessageDiv.style.display = 'none';
              window.location.reload(); // Refresh the page after 3 seconds to show updates.
            }, 3000);
          }
          // Clear the form
          amenityForm.reset();
        })
        .catch(error => {
          console.error('[Amenity] Error adding amenity:', error);
          if (errorMessageDiv) {
            errorMessageDiv.textContent = error.message || 'An error occurred while adding the amenity.';
            errorMessageDiv.style.color = 'red';
            errorMessageDiv.style.display = 'block';
            setTimeout(() => {
              errorMessageDiv.style.display = 'none';
            }, 3000);
          }
        });
      });
    }
  });
  