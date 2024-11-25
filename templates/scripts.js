document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message'); // Assuming an error message element exists

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await loginUser(email, password);
        
        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          alert('Login failed: ' + response.statusText);
        }
      } catch (error) {
        console.error('Error logging in:', error);
        if (errorMessage) {
          errorMessage.style.display = 'block';
          errorMessage.textContent = 'An unexpected error occurred. Please try again later';
        }
      }
    });
  }
});

async function loginUser(email, password) {
  return fetch('https://your-api-url/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password }) // Send credentials as JSON
  });
}

// Fetch places data 
async function fetchPlaces() {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });
    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      console.error("Failed to fetch places:", response.statusText);
    }
  } catch (error) {
    console.error("Error fetching places:", error);
  }
}

// Dynamically populate list of places
function displayPlaces(places) {
  const placesList = document.getElementById("places-list");
  placesList.innerHTML = "";

  places.forEach(place => {
    const placeDiv = document.createElement("div"); 
    placeDiv.className = "place-item";
    placeDiv.innerHTML = `
      <h2>${place.name}</h2>
      <p>${place.description}</p>
      <p><strong>Price:</strong>${place.price}</p>
    `;
    placeDiv.dataset.price = place.price;
    placesList.appendChild(placeDiv);
  });
}

function filterPlacesByPrice(maxPrice) {
  const placeItems = document.querySelectorAll(".place-item");
   
  placeItems.forEach((item) => {
    const placePrice = parseFloat(item.dataset.price);
    if (maxPrice == "all" || placePrice <= maxPrice) {
      item.style.display = "block";
    } else {
      item.style.display = "none";
    }
  });
}

document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedValue = event.target.value;
  filterPlacesByPrice(selectedValue == "all" ? "all" : parseFloat(selectedValue));
});

// Place Details
document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  
  fetchPlaceDetails(place_id);
});

function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('place_id');
}

// Fetch place details
async function fetchPlaceDetails(place_id) {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${place_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      console.error("Failed to fetch place details");
    }
}

function displayPlaceDetails(place) {
  const placeDetailsSection = document.getElementById('place-details');
  placeDetailsSection.innerHTML = '';

  const placeName = document.createElement('h2');
  placeName.textContent = place.name;

  const placeDescription = document.createElement('p');
  placeDescription.textContent = place.description;

  const placePrice = document.createElement('p');
  placePrice.textContent = `Price: $${place.price}`;

  const amenitiesList = document.createElement('ul');
  place.amenities.forEach(amenity => {
    const listItem = document.createElement('li');
    listItem.textContent = amenity;
    amenitiesList.appendChild(listItem);
  });

  const reviewsList = document.createElement('ul');
  place.reviews.forEach(review => {
    const reviewItem = document.createElement('li');
    reviewItem.textContent = `${review.comment}`;
    reviewsList.appendChild(reviewItem);
  });

  placeDetailsSection.appendChild(placeName);
  placeDetailsSection.appendChild(placeDescription);
  placeDetailsSection.appendChild(placePrice);
  placeDetailsSection.appendChild(amenitiesList);
  placeDetailsSection.appendChild(reviewsList);
}
