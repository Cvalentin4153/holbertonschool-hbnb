/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    // Check authentication and update UI accordingly
    console.log('Page loaded, checking authentication...');
    
    const token = getToken();
    console.log('Token on page load:', token ? 'Found' : 'Not found');
    
    // Update the login button immediately
    updateLoginButton();
    
    // Also set a short timeout to update it again (in case of any race conditions)
    setTimeout(updateLoginButton, 500);
    
    // Check which page we're on
    if (window.location.pathname.includes('place.html')) {
        // Get place ID from URL
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        
        if (placeId) {
            loadPlaceDetails(placeId);
            loadPlaceReviews(placeId);
        } else {
            window.location.href = 'index.html';
        }
    } else if (window.location.pathname.endsWith('/index.html') || 
               window.location.pathname.endsWith('/') || 
               window.location.pathname.endsWith('/Front-End/base_files/')) {
        // Load places for the main page
        fetchPlaces();
    }
    
    // Handle price filter changes
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        // Make sure the options match the requirements (10, 50, 100, All)
        priceFilter.innerHTML = '';
        
        // Add price filter options in the correct order
        const priceOptions = [
            { value: '100', text: '$100' },
            { value: '150', text: '$150' },
            { value: '200', text: '$200' },
            { value: 'all', text: 'All' }
        ];
        
        priceOptions.forEach(option => {
            const optionElem = document.createElement('option');
            optionElem.value = option.value;
            optionElem.textContent = option.text;
            if (option.value === 'all') {
                optionElem.selected = true;
            }
            priceFilter.appendChild(optionElem);
        });
        
        // Add event listener for price filter changes
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }

    // Handle review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            if (!isLoggedIn()) {
                alert('You must be logged in to submit a review.');
                window.location.href = 'login.html';
                return;
            }
            
            const urlParams = new URLSearchParams(window.location.search);
            const placeId = urlParams.get('id');
            
            if (!placeId) {
                alert('Invalid place ID.');
                return;
            }
            
            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;
            
            try {
                const response = await fetch(`http://127.0.0.1:5001/api/v1/reviews/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getToken()}`
                    },
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(rating, 10),
                        place_id: placeId
                    })
                });
                
                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                    loadPlaceReviews(placeId);
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.error || 'Failed to submit review'}`);
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('Network error. Please try again later.');
            }
        });
    }

    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        // For testing, populate the form with sample credentials
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        
        if (emailInput && passwordInput) {
            emailInput.value = 'admin@example.com';
            passwordInput.value = 'admin123';
        }
        
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = emailInput.value;
            const password = passwordInput.value;
            
            // Clear any existing error messages
            clearError();
            
            // Show loading indicator
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'loading-message';
            loadingMessage.textContent = 'Logging in...';
            loginForm.insertBefore(loadingMessage, loginForm.querySelector('button'));
            
            try {
                const response = await fetch('http://127.0.0.1:5001/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                // Remove loading indicator
                loadingMessage.remove();

                if (response.ok) {
                    const data = await response.json();
                    console.log('Login successful!', data);
                    
                    // Store the token in a cookie 
                    document.cookie = `token=${data.access_token}; path=/;`;
                    console.log('Token stored in cookie:', data.access_token);
                    
                    // Also store in localStorage for redundancy
                    localStorage.setItem('token', data.access_token);
                    console.log('Token stored in localStorage');
                    
                    // Store user info in localStorage for easy access
                    localStorage.setItem('user', JSON.stringify(data.user));
                    
                    // Show success message
                    showSuccess('Login successful! Redirecting...');
                    
                    // Redirect to main page after a short delay
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1000);
                } else {
                    const errorData = await response.json();
                    showError(errorData.error || 'Login failed. Please try again.');
                }
            } catch (error) {
                // Remove loading indicator
                loadingMessage.remove();
                showError('Network error. Please try again later.');
                console.error('Login error:', error);
            }
        });
    }
    
    // Function to load place details
    async function loadPlaceDetails(placeId) {
        const placeLoading = document.getElementById('place-loading');
        const placeContent = document.getElementById('place-content');
        
        if (!placeLoading || !placeContent) return;
        
        try {
            const headers = {};
            const token = getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch(`http://127.0.0.1:5001/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: headers
            });
            
            if (response.ok) {
                const place = await response.json();
                
                // Update place details
                document.title = `${place.title || place.name || 'Place Details'} - HBnB`;
                document.getElementById('place-title').textContent = place.title || place.name || 'Place Details';
                
                // Handle owner data if available through separate request or nested
                if (place.owner) {
                    document.getElementById('place-host').innerHTML = `<strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}`;
                } else if (place.owner_id) {
                    document.getElementById('place-host').innerHTML = `<strong>Host:</strong> ID: ${place.owner_id}`;
                } else {
                    document.getElementById('place-host').innerHTML = '<strong>Host:</strong> Unknown';
                }
                
                document.getElementById('place-price').innerHTML = `<strong>Price per night:</strong> $${place.price || place.price_per_night || 'N/A'}`;
                document.getElementById('place-description').innerHTML = `<strong>Description:</strong> ${place.description || 'No description available'}`;
                
                // Handle amenities
                if (place.amenities && place.amenities.length > 0) {
                    if (typeof place.amenities[0] === 'object') {
                        // If amenities are objects with name property
                        const amenityNames = place.amenities.map(amenity => amenity.name).join(', ');
                        document.getElementById('place-amenities').innerHTML = `<strong>Amenities:</strong> ${amenityNames}`;
                    } else {
                        // If amenities are strings or IDs
                        document.getElementById('place-amenities').innerHTML = `<strong>Amenities:</strong> ${place.amenities.join(', ')}`;
                    }
                } else {
                    document.getElementById('place-amenities').innerHTML = '<strong>Amenities:</strong> None';
                }
                
                // Show review form if logged in
                if (isLoggedIn()) {
                    const addReviewContainer = document.getElementById('add-review-container');
                    if (addReviewContainer) {
                        addReviewContainer.style.display = 'block';
                    }
                }
                
                // Show content, hide loading
                placeLoading.style.display = 'none';
                placeContent.style.display = 'block';
                
                // Keep place data for reviews
                placeContent.dataset.placeData = JSON.stringify(place);
            } else {
                placeLoading.textContent = 'Error loading place details. Place may not exist.';
            }
        } catch (error) {
            console.error('Error loading place details:', error);
            placeLoading.textContent = 'Network error. Please check your connection.';
        }
    }
    
    // Function to load place reviews
    async function loadPlaceReviews(placeId) {
        const reviewsList = document.getElementById('reviews-list');
        if (!reviewsList) return;
        
        reviewsList.innerHTML = '<div class="loading-message">Loading reviews...</div>';
        
        try {
            const response = await fetch(`http://127.0.0.1:5001/api/v1/reviews/?place_id=${placeId}`, {
                method: 'GET'
            });
            
            if (response.ok) {
                const reviews = await response.json();
                
                if (reviews.length === 0) {
                    reviewsList.innerHTML = '<p>No reviews yet. Be the first to leave a review!</p>';
                    return;
                }
                
                reviewsList.innerHTML = '';
                
                reviews.forEach(review => {
                    const reviewCard = document.createElement('div');
                    reviewCard.className = 'review-card';
                    
                    const userName = document.createElement('p');
                    userName.innerHTML = `<strong>${review.user ? review.user.first_name + ' ' + review.user.last_name : 'Anonymous'}:</strong>`;
                    
                    const reviewText = document.createElement('p');
                    reviewText.textContent = review.text || 'No comment';
                    
                    const rating = document.createElement('p');
                    rating.className = 'rating';
                    rating.innerHTML = `Rating: ${getStarRating(review.rating)}`;
                    
                    reviewCard.appendChild(userName);
                    reviewCard.appendChild(reviewText);
                    reviewCard.appendChild(rating);
                    
                    reviewsList.appendChild(reviewCard);
                });
            } else {
                reviewsList.innerHTML = '<div class="error-message">Error loading reviews</div>';
            }
        } catch (error) {
            console.error('Error loading reviews:', error);
            reviewsList.innerHTML = '<div class="error-message">Network error. Please check your connection.</div>';
        }
    }
    
    // Function to display error messages
    function showError(message) {
        clearError();
        
        // Create and show new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        if (loginForm) {
            loginForm.insertBefore(errorDiv, loginForm.firstChild);
        }
    }
    
    // Function to clear error messages
    function clearError() {
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        const existingSuccess = document.querySelector('.success-message');
        if (existingSuccess) {
            existingSuccess.remove();
        }
    }
    
    // Function to display success messages
    function showSuccess(message) {
        clearError();
        
        // Create and show success message
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        
        if (loginForm) {
            loginForm.insertBefore(successDiv, loginForm.firstChild);
        }
    }
    
    // Function to get token from cookie
    function getToken() {
        console.log('Checking for token in cookies');
        console.log('All cookies:', document.cookie);
        
        const cookies = document.cookie.split(';');
        let token = null;
        
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('token=')) {
                token = cookie.substring('token='.length);
                console.log('Token found in cookies');
                break;
            }
        }
        
        // If no token in cookies, check localStorage as fallback
        if (!token) {
            const localToken = localStorage.getItem('token');
            if (localToken) {
                console.log('Token found in localStorage');
                token = localToken;
            }
        }
        
        if (!token) {
            console.log('No token found');
        }
        
        return token;
    }
    
    // Check if user is logged in
    function isLoggedIn() {
        return getToken() !== null;
    }
    
    // Update login/logout button
    function updateLoginButton() {
        const loginButton = document.querySelector('.login-button');
        if (loginButton) {
            console.log('Updating login button, isLoggedIn:', isLoggedIn());
            
            // Remove any existing click event listeners
            const newLoginButton = loginButton.cloneNode(true);
            loginButton.parentNode.replaceChild(newLoginButton, loginButton);
            
            if (isLoggedIn()) {
                console.log('User is logged in, changing to Logout');
                newLoginButton.textContent = 'Logout';
                newLoginButton.href = '#';
                newLoginButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    console.log('Logout clicked');
                    
                    // Clear all storage locations
                    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                    localStorage.removeItem('token');
                    localStorage.removeItem('user');
                    
                    console.log('All tokens cleared');
                    console.log('Cookies after logout:', document.cookie);
                    
                    // Reload the page to update UI
                    window.location.reload();
                });
            } else {
                console.log('User is not logged in, keeping as Login');
                newLoginButton.textContent = 'Login';
                newLoginButton.href = 'login.html';
            }
        } else {
            console.error('Login button not found in the DOM');
        }
    }
    
    // Helper function to get star rating HTML
    function getStarRating(rating) {
        rating = parseInt(rating, 10) || 0;
        if (rating < 1) rating = 1;
        if (rating > 5) rating = 5;
        
        const fullStars = '★'.repeat(rating);
        const emptyStars = '☆'.repeat(5 - rating);
        
        return fullStars + emptyStars;
    }
    
    // Fetch places from API
    async function fetchPlaces() {
        const placesListElement = document.getElementById('places-list');
        if (!placesListElement) return;
        
        console.log('Fetching places...');
        
        // Clear existing places
        placesListElement.innerHTML = '<div class="loading-message">Loading places...</div>';
        
        try {
            const headers = {
                'Content-Type': 'application/json'
            };
            const token = getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
                console.log('Using token for authentication');
            }
            
            console.log('Sending request to API...');
            
            const response = await fetch('http://127.0.0.1:5001/api/v1/places/', {
                method: 'GET',
                headers: headers
            });
            
            console.log('Response status:', response.status);
            
            if (response.ok) {
                const places = await response.json();
                console.log('Places fetched:', places.length);
                
                displayPlaces(places);
                
                // Keep a copy of all places in a data attribute for filtering
                placesListElement.dataset.allPlaces = JSON.stringify(places);
            } else {
                console.error('Failed to fetch places:', response.statusText);
                placesListElement.innerHTML = '<div class="error-message">Failed to load places. Please try again later.</div>';
            }
        } catch (error) {
            console.error('Error fetching places:', error);
            placesListElement.innerHTML = '<div class="error-message">Network error. Please check your connection.</div>';
        }
    }
    
    // Display places in the UI
    function displayPlaces(places) {
        const placesListElement = document.getElementById('places-list');
        if (!placesListElement) return;
        
        placesListElement.innerHTML = '';
        
        if (places.length === 0) {
            placesListElement.innerHTML = '<div class="no-places">No places available</div>';
            return;
        }
        
        places.forEach(place => {
            const placeCard = document.createElement('div');
            placeCard.className = 'place-card';
            placeCard.dataset.price = place.price || 0;
            
            const placeTitle = document.createElement('h2');
            placeTitle.textContent = place.title || place.name || 'Unnamed Place';
            
            const placePrice = document.createElement('p');
            placePrice.textContent = `Price per night: $${place.price || place.price_per_night || 'N/A'}`;
            
            const detailsButton = document.createElement('button');
            detailsButton.type = 'button';
            detailsButton.className = 'details-button';
            detailsButton.textContent = 'View Details';
            detailsButton.addEventListener('click', () => {
                window.location.href = `place.html?id=${place.id}`;
            });
            
            placeCard.appendChild(placeTitle);
            placeCard.appendChild(placePrice);
            placeCard.appendChild(detailsButton);
            
            placesListElement.appendChild(placeCard);
        });
    }
    
    // Filter places by price
    function filterPlacesByPrice(maxPrice) {
        const placesListElement = document.getElementById('places-list');
        if (!placesListElement || !placesListElement.dataset.allPlaces) return;
        
        const allPlaces = JSON.parse(placesListElement.dataset.allPlaces);
        
        // If "All" is selected, show all places
        if (maxPrice === 'all') {
            displayPlaces(allPlaces);
            return;
        }
        
        // Convert to number for comparison
        const maxPriceNum = parseInt(maxPrice, 10);
        
        // Filter places by price
        const filteredPlaces = allPlaces.filter(place => {
            const placePrice = parseInt(place.price || place.price_per_night || 0, 10);
            return placePrice <= maxPriceNum;
        });
        
        displayPlaces(filteredPlaces);
    }
});