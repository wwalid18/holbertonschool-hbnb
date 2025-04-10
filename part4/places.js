// places.js
document.addEventListener('DOMContentLoaded', () => {
  // -------------------------------------
  // Utility Function: Get Cookie by Name
  // (Reproduced here for independence)
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
    let placesContainer = document.getElementById('places-container');
    if (!placesContainer) {
      placesContainer = document.createElement('div');
      placesContainer.id = 'places-container';
      placesSection.appendChild(placesContainer);
    }
    
    let allPlaces = [];

    // NOTE: Updated URL now includes a trailing slash to prevent redirects.
    async function fetchPlaces() {
      const token = getCookie('token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      try {
        const response = await fetch('http://localhost:5000/api/v1/places/', {
          method: 'GET',
          headers: headers
        });
        if (!response.ok) {
          throw new Error('Failed to fetch places');
        }
        const data = await response.json();
        console.log('[Places] Fetched places:', data);
        return data; // Expected to be an array of place objects.
      } catch (error) {
        console.error('[Places] Error fetching places:', error);
        return [];
      }
    }

    function renderPlaces(places) {
      placesContainer.innerHTML = '';
      places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('place-card');
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

    async function initializePlaces() {
      allPlaces = await fetchPlaces();
      renderPlaces(allPlaces);
    }
    initializePlaces();

    // -----------------------------------------------------------
    // Client-Side Filtering by Price Using element.style.display
    // -----------------------------------------------------------
    // Expected dropdown options: 10, 50, 100, All.
    const filterSelect = document.getElementById('max-price');
    if (filterSelect) {
      filterSelect.addEventListener('change', () => {
        const selectedValue = filterSelect.value;
        console.log('[Places] Filter selected:', selectedValue);
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
