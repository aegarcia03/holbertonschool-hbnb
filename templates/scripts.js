document.addEventListener("DOMContentLoaded", function() {
   
    const currentPage = window.location.pathname;

    // Logic for place.html
    if (currentPage.includes('index.html')) {
        document.getElementById('price-filter').addEventListener('change', (event) => {
            const selectedPrice = event.target.value; // Get the selected price range
            const places = document.querySelectorAll(".place-card"); // Select all place cards

            places.forEach(place => {
                const priceElement = place.querySelector('.price span'); // Fix selector for price span
                const price = parseFloat(priceElement.textContent.replace(/[^0-9.]/g, '')); // Extract numeric value

                // Show or hide places based on the filter
                if (selectedPrice === "all" || price <= parseFloat(selectedPrice)) {
                    place.style.display = "block";  // Show matching places
                } else {
                    place.style.display = "none";  // Hide non-matching places
                }
            });
        });
    }

    // Logic for add_review.html
    if (currentPage.includes('add_review.html')) {
        // Get Place ID from the URL query string
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id'); // Assuming the URL looks like `?place_id=some-place-id`

        // Review form and message elements
        const reviewForm = document.getElementById('review-form');
        const reviewText = document.getElementById('review-text');
        const messageDiv = document.getElementById('message');

        // Handle form submission
        reviewForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission behavior

            // Get the review text
            const review = reviewText.value.trim();

            // Check if review is empty
            if (!review) {
                showMessage('Please write a review.', 'error');
                return;
            }

            // Prepare data for the POST request
            const reviewData = {
                review_text: review,
                place_id: placeId
            };

            // Send review data via Fetch API (POST request)
            fetch(`http://127.0.0.1:5001/api/v1/places/${placeId}/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(reviewData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Error submitting review'); });
                }
                return response.json();
            })
            .then(data => {
                // Display success message and clear form
                showMessage('Review submitted successfully!', 'success');
                reviewText.value = ''; // Clear the review text area
            })
            .catch(error => {
                // Display error message
                showMessage(error.message, 'error');
            });
        });

        // Function to display success or error message
        function showMessage(message, type) {
            messageDiv.style.display = 'block';
            messageDiv.textContent = message;
            messageDiv.style.color = type === 'success' ? 'green' : 'red';
        }
    }
});
