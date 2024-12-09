document.addEventListener("DOMContentLoaded", () => {
    const priceFilter = document.getElementById('price-filter');
    const searchBar = document.getElementById('search-bar');
    const places = document.querySelectorAll('.place-card');

    // Function to filter places based on price and search query
    function filterPlaces() {
        const selectedPrice = priceFilter.value; // Get selected price
        const searchQuery = searchBar.value.toLowerCase().trim(); // Get search query, converted to lowercase

        places.forEach(place => {
            const priceElement = place.querySelector('.price span');
            const price = parseFloat(priceElement.textContent.replace(/[^0-9.]/g, '')); // Ensure we get the numeric value
            const placeTitle = place.querySelector('.card-header h3').textContent.toLowerCase(); // Get place title and convert to lowercase

            let matchesPrice = false;
            // Show or hide based on price filter
            switch(selectedPrice) {
                case '1': // Under $10
                    matchesPrice = price <= 10;
                    break;
                case '2': // Under $50
                    matchesPrice = price <= 50;
                    break;
                case '3': // Under $100
                    matchesPrice = price <= 100;
                    break;
                default: // Show all
                    matchesPrice = true;
            }

            // Show place only if both price and search conditions are matched
            if (matchesPrice && placeTitle.includes(searchQuery)) {
                place.style.display = 'block'; // Show matching places
            } else {
                place.style.display = 'none'; // Hide non-matching places
            }
        })
    }

    // Price filter event listener
    priceFilter.addEventListener('change', filterPlaces);

    // Search bar event listener
    searchBar.addEventListener('input', filterPlaces); // Trigger filtering on input change
});
