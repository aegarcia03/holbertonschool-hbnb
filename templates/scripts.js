document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedPrice = event.target.value; // Get the selected price range
    const places = document.querySelectorAll(".place-card"); // Select all place cards

    places.forEach(place => {
        const priceElement = place.querySelector('.price'); // Find the price element
        const price = parseFloat(priceElement.textContent.replace(/[^0-9.]/g, '')); // Extract numeric value

        // Show or hide places based on the filter
        if (selectedPrice === "all" || price <= parseFloat(selectedPrice)) {
            place.style.display = "block";  // Show matching places
        } else {
            place.style.display = "none";  // Hide non-matching places
        }
    });
});
