document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedPrice = event.target.value;
    const places = document.querySelectorAll(".place-card");

    places.forEach(place => {
        const price = parseInt(place.querySelector('p').textContent.split('$')[1]);

        if (selectedPrice == "all" || price <= parseInt(selectedPrice)) {
            place.style.display = "block";  // Show the place if it matches filter
        } else {
            place.style.display = "none";  // Hide the place if it doesn't match
        }
    });
});