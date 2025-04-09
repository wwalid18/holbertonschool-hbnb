// places.js
document.addEventListener('DOMContentLoaded', () => {
  // -------------------------------------
  // Utility Function: Get Cookie by Name
  // (You can reuse this from auth.js if you modularize further, but included here for independence.)
  // -------------------------------------
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(';').shift();
    }
    return null;
  };

  // -----------------------------------------------------------
  // Fetch Places Data and Populate the Places List (index.html)
  // -----------------------------------------------------------
  const placesSection = document.getElementById('places-list');
  if (placesSection) {
    // Create a container element inside #places-list if not already present.
    let placesContainer = document.getElementById('places-container');
    if (!placesContainer) {
      placesContainer = document.createElement('div');
      placesContainer.id = 'places-container';
      placesSection.appendChild(placesContainer);
    }
    
    // Global variable to store all fetched places.
    let allPlaces = [];

    // Function to fetch places from the API, including the JWT token if available.
    async function fetchPlaces() {
      const token = getCookie('token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
          method: 'GET',
          headers: headers
        });
        if (!response.ok) {
          throw new Error('Failed to fetch places');
        }
        const data = await response.json();
        return data; // Expected to be an array of place objects.
      } catch (error) {
        console.error('Error fetching places:', error);
        return [];
      }
    }

    // Function to dynamically render place cards into the places container.
    function renderPlaces(places) {
      // Clear any existing content.
      placesContainer.innerHTML = '';
      places.forEach(place => {
        // Create a card element for the place.
        const card = document.createElement('div');
        card.classList.add('place-card');
        // Set a data attribute for price (for filtering).
        card.setAttribute('data-price', place.price);
        card.innerHTML = `
          <h3>${place.title}</h3>
          <p>${place.description || 'No description provided.'}</p>
          <p><strong>Price per night:</strong> $${place.price}</p>
          <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
          <button class="details-button" onclick="window.location.href='place.html?placeId=${place.id}'">View Details</button>
        `;
        placesContainer.appendChild(card);
      });
    }

    // Initialize the page by fetching and rendering the list of places.
    async function initializePlaces() {
      allPlaces = await fetchPlaces();
      renderPlaces(allPlaces);
    }
    initializePlaces();

    // -----------------------------------------------------------
    // Client-Side Filtering by Price Using element.style.display
    // -----------------------------------------------------------
    // The dropdown should be loaded with the following options: 10, 50, 100, All.
    const filterSelect = document.getElementById('max-price');
    if (filterSelect) {
      filterSelect.addEventListener('change', () => {
        const selectedValue = filterSelect.value; // Expected values: "10", "50", "100", or "All"
        // Get all the place card elements.
        const placeCards = document.querySelectorAll('.place-card');
        placeCards.forEach(card => {
          const price = parseFloat(card.getAttribute('data-price'));
          if (selectedValue === "All" || price <= parseFloat(selectedValue)) {
            card.style.display = 'block';
          } else {
            card.style.display = 'none';
          }
        });
      });
    }
  }
});
