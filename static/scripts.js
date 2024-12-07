document.addEventListener("DOMContentLoaded", () => {
    const priceFilter = document.getElementById('price-filter');
    const places = document.querySelectorAll('.place-card');

    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value; // Get selected price

        places.forEach(place => {
            const priceElement = place.querySelector('.price span');
            const price = parseFloat(priceElement.textContent.replace(/[^0-9.]/g, '')); // Ensure we get the numeric value

            // Show or hide based on filter
            switch(selectedPrice) {
                case '1': // Under $10
                    if (price <= 10) {
                        place.style.display = 'block'; // Show matching places
                    } else {
                        place.style.display = 'none'; // Hide non-matching places
                    }
                    break;
                case '2': // Under $50
                    if (price <= 50) {
                        place.style.display = 'block'; 
                    } else {
                        place.style.display = 'none';
                    }
                    break;
                case '3': // Under $100
                    if (price <= 100) {
                        place.style.display = 'block';
                    } else {
                        place.style.display = 'none';
                    }
                    break;
                default: // Show all
                    if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                        place.style.display = 'block'; // Show matching places
                    } else {
                        place.style.display = 'none'; // Hide non-matching places
                    }
                    break;
            }
        });
    });
});
