document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const logoutButton = document.getElementById('logout-button');
  const priceFilter = document.getElementById('price-filter');
  const createPlaceBtn = document.getElementById('create-place-btn');

  // Always check authentication status
  checkAuthentication();

  // Additional setup for index page
  if (document.getElementById('places-list')) {
    // Set up price filter listener
    if (priceFilter) {
      priceFilter.addEventListener('change', (e) => {
        console.log('Price filter changed:', e.target.value);
        filterPlacesByPrice(e.target.value);
      });
    }
    // Fetch places
    fetchPlaces();
  }

  // Set up Create Place button
  if (createPlaceBtn) {
    console.log('Create Place button found, adding click handler');
    createPlaceBtn.addEventListener('click', function() {
      console.log('Create Place button clicked');
      window.location.href = 'add-place.html';
    });
  } else {
    console.log('Create Place button not found');
  }

  if (logoutButton) {
    logoutButton.addEventListener('click', (event) => {
      event.preventDefault();
      logout();
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      document.getElementById('error-message').textContent = '';
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }

  if (signupForm) {
    signupForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      document.getElementById('error-message').textContent = '';
      const firstName = document.getElementById('first-name').value;
      const lastName = document.getElementById('last-name').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirm-password').value;

      if (password !== confirmPassword) {
        document.getElementById('error-message').textContent = 'Passwords do not match';
        return;
      }

      await signupUser(firstName, lastName, email, password);
    });
  }

  // Add place form submission
  const addPlaceForm = document.getElementById('add-place-form');
  if (addPlaceForm) {
    addPlaceForm.addEventListener('submit', async function(e) {
      e.preventDefault();
  
      const token = getCookie('token');
      console.log('Token for place creation:', token ? 'exists' : 'missing');
      
      if (!token) {
        console.log('No token found, redirecting to login page');
        window.location.href = 'login.html';
        return;
      }
  
      // Get all checked amenities
      const checkedAmenities = Array.from(document.querySelectorAll('input[name="amenities"]:checked'))
        .map(checkbox => checkbox.value);
  
      // Create the place data with all required fields
      const formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        price: parseFloat(document.getElementById('price').value),
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value),
        amenities: checkedAmenities
      };

      // Log the complete request data
      console.log('Complete request data:', {
        url: 'http://127.0.0.1:5001/api/v1/places/',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });
  
      try {
        const response = await fetch('http://127.0.0.1:5001/api/v1/places/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(formData)
        });
  
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        
        if (response.ok) {
          alert('Place added successfully!');
          window.location.href = 'index.html';
        } else {
          const errorMessage = document.getElementById('error-message');
          // Log the complete error response
          console.error('Error response:', {
            status: response.status,
            statusText: response.statusText,
            data: data
          });
          
          // Display more detailed error message if available
          if (data.errors) {
            const errorDetails = Object.entries(data.errors)
              .map(([field, errors]) => `${field}: ${errors.join(', ')}`)
              .join('\n');
            errorMessage.textContent = `Validation error:\n${errorDetails}`;
          } else if (data.traceback) {
            // For 500 errors with traceback
            console.error('Server error traceback:', data.traceback);
            errorMessage.textContent = `Server error: ${data.error}\nCheck console for details.`;
          } else {
            errorMessage.textContent = data.error || 'Error adding place. Please check the console for details.';
          }
          errorMessage.style.display = 'block';
        }
      } catch (error) {
        console.error('Error during place creation:', error);
        console.error('Error stack:', error.stack);
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = 'Error adding place. Please check the console for details.';
        errorMessage.style.display = 'block';
      }
    });
  }

  // Check if user is logged in and update UI accordingly
  function checkLoginStatus() {
    const token = getCookie('token');
    const loginBtn = document.getElementById('login-btn');
    const signupBtn = document.getElementById('signup-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const createPlaceBtn = document.getElementById('create-place-btn');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    
    console.log('Checking login status, token:', token ? 'exists' : 'does not exist');
    console.log('Create Place button:', createPlaceBtn ? 'found' : 'not found');
    
    if (token) {
      // User is logged in
      if (loginBtn) loginBtn.style.display = 'none';
      if (signupBtn) signupBtn.style.display = 'none';
      if (logoutBtn) logoutBtn.style.display = 'inline-block';
      if (createPlaceBtn) {
        createPlaceBtn.style.display = 'inline-block';
        console.log('Showing Create Place button');
      }
      if (loginLink) loginLink.style.display = 'none';
      if (logoutButton) logoutButton.style.display = 'inline-block';
    } else {
      // User is not logged in
      if (loginBtn) loginBtn.style.display = 'inline-block';
      if (signupBtn) signupBtn.style.display = 'inline-block';
      if (logoutBtn) logoutBtn.style.display = 'none';
      if (createPlaceBtn) {
        createPlaceBtn.style.display = 'none';
        console.log('Hiding Create Place button');
      }
      if (loginLink) loginLink.style.display = 'inline-block';
      if (logoutButton) logoutButton.style.display = 'none';
    }
  }

  // Add event listener for the Create Place button
  document.addEventListener('DOMContentLoaded', function() {
    const createPlaceBtn = document.getElementById('create-place-btn');
    if (createPlaceBtn) {
      createPlaceBtn.addEventListener('click', function() {
        window.location.href = 'add-place.html';
      });
    }
    
    // Check login status when page loads
    checkLoginStatus();
  });
});

async function loginUser(email, password) {
  const errorMessageElement = document.getElementById('error-message');
  console.log('Attempting login with:', { email });

  try {
    const response = await fetch('http://127.0.0.1:5001/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    console.log('Login response status:', response.status);
    const data = await response.json();
    console.log('Login response data:', data);

    if (response.ok) {
      // Store the access_token in a cookie (note: changed from data.token to data.access_token)
      const token = data.access_token;
      console.log('Token received:', token ? 'yes' : 'no');
      
      if (token) {
        // Set cookie with proper attributes
        document.cookie = `token=${token}; path=/; secure; samesite=Strict`;
        console.log('Token stored in cookie');
        
        // Verify the token was stored
        const storedToken = getCookie('token');
        console.log('Stored token verification:', storedToken ? 'success' : 'failed');
      } else {
        console.error('No token in login response');
        if (errorMessageElement) {
          errorMessageElement.textContent = 'Login failed: No token received';
          errorMessageElement.style.display = 'block';
        }
        return;
      }
      
      console.log('Login successful, redirecting...');
      
      // Check authentication before redirecting
      checkAuthentication();
      
      window.location.href = 'index.html';
    } else {
      if (errorMessageElement) {
        errorMessageElement.textContent = data.error || 'Login failed. Please check your credentials.';
        errorMessageElement.style.display = 'block';
      }
      console.error('Login failed:', data.error);
    }
  } catch (error) {
    console.error('Error during login:', error);
    if (errorMessageElement) {
      errorMessageElement.textContent = 'An error occurred during login. Please try again.';
      errorMessageElement.style.display = 'block';
    }
  }
}

async function signupUser(firstName, lastName, email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5001/api/v1/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password
      })
    });

    const data = await response.json();
    
    if (response.ok) {
      window.location.href = 'login.html';
    } else {
      document.getElementById('error-message').textContent = data.error || 'Failed to create account';
    }
  } catch (error) {
    console.error('Signup error:', error);
    document.getElementById('error-message').textContent = 'An error occurred. Please try again.';
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    const cookieValue = parts.pop().split(';').shift();
    console.log(`Cookie ${name} value:`, cookieValue ? 'exists' : 'not found');
    return cookieValue;
  }
  console.log(`Cookie ${name} not found`);
  return null;
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutButton = document.getElementById('logout-button');
  const createPlaceBtn = document.getElementById('create-place-btn');
  const currentPage = window.location.pathname;

  console.log('Checking authentication on page:', currentPage);
  console.log('Token:', token ? 'exists' : 'does not exist');

  // If we're on login or signup page, don't show either button
  if (currentPage.includes('login.html') || currentPage.includes('signup.html')) {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutButton) logoutButton.style.display = 'none';
    if (createPlaceBtn) createPlaceBtn.style.display = 'none';
    
    // If user is already logged in, redirect to index
    if (token) {
      window.location.href = 'index.html';
    }
    return;
  }

  // For other pages (like index.html)
  if (!token) {
    if (loginLink) {
      loginLink.style.display = 'block';
      console.log('Showing login link');
    }
    if (logoutButton) {
      logoutButton.style.display = 'none';
      console.log('Hiding logout button');
    }
    if (createPlaceBtn) {
      createPlaceBtn.style.display = 'none';
      console.log('Hiding create place button');
    }
  } else {
    if (loginLink) {
      loginLink.style.display = 'none';
      console.log('Hiding login link');
    }
    if (logoutButton) {
      logoutButton.style.display = 'block';
      console.log('Showing logout button');
    }
    if (createPlaceBtn) {
      createPlaceBtn.style.display = 'inline-block';
      console.log('Showing create place button');
    }
  }
}

function clearCookies() {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i];
    const eqPos = cookie.indexOf('=');
    const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
  }
  console.log('All cookies cleared');
}

function logout() {
  clearCookies();
  window.location.href = 'login.html';
}

let places = [];
let currentPriceFilter = 'all';

async function fetchPlaces() {
  const loadingMessage = document.querySelector('.loading-message');
  const placesList = document.querySelector('.places-list');
  const token = getCookie('token');
  
  try {
    loadingMessage.style.display = 'block';
    placesList.innerHTML = '';

    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch('http://127.0.0.1:5001/api/v1/places/', {
      method: 'GET',
      headers: headers
    });

    if (response.status === 401) {
      // Token is invalid or expired
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.href = 'login.html';
      return;
    }

    if (!response.ok) {
      throw new Error('Failed to fetch places');
    }

    places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error fetching places:', error);
    placesList.innerHTML = '<p class="error">Error loading places. Please try again later.</p>';
  } finally {
    loadingMessage.style.display = 'none';
  }
}

function displayPlaces(placesToShow) {
  const placesList = document.querySelector('.places-list');
  placesList.innerHTML = '';

  if (!placesToShow || placesToShow.length === 0) {
    placesList.innerHTML = '<p class="no-results">No places found matching your criteria.</p>';
    return;
  }

  placesToShow.forEach(place => {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.innerHTML = `
      <h3>${place.title || 'Unnamed Place'}</h3>
      <p class="description">${place.description || 'No description available'}</p>
      <p class="price">Price per night: $${place.price || 0}</p>
      <button class="view-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;
    placesList.appendChild(placeCard);
  });
}

function filterPlacesByPrice(maxPrice) {
  console.log('Filtering places by price:', maxPrice);
  const placesList = document.querySelector('.places-list');
  let filteredPlaces = places;

  if (maxPrice !== 'all') {
    maxPrice = parseFloat(maxPrice);
    filteredPlaces = places.filter(place => {
      const price = parseFloat(place.price);
      console.log(`Checking place price: ${price} against max: ${maxPrice}`);
      return price <= maxPrice;
    });
  }

  console.log('Filtered places:', filteredPlaces);
  displayPlaces(filteredPlaces);
}

async function createPlace(event) {
    event.preventDefault();
    const token = getCookie('token');
    console.log('Token exists:', !!token);

    if (!token) {
        console.log('No token found, redirecting to login');
        window.location.href = 'login.html';
        return;
    }

    const form = event.target;
    const checkedAmenities = Array.from(document.querySelectorAll('input[name="amenities"]:checked'))
        .map(checkbox => checkbox.value);

    const formData = {
        title: form.title.value,
        description: form.description.value,
        price: parseFloat(form.price.value),
        latitude: parseFloat(form.latitude.value),
        longitude: parseFloat(form.longitude.value)
    };

    console.log('Submitting place data:', formData);

    try {
        const response = await fetch('http://127.0.0.1:5001/api/v1/places/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log('Response status:', response.status);
        console.log('Response data:', data);

        if (!response.ok) {
            let errorMessage = 'Failed to create place. ';
            if (data.msg === 'Subject must be a string') {
                errorMessage += 'Authentication error. Please try logging in again.';
                // Clear the invalid token
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
            } else {
                errorMessage += data.message || data.msg || 'Unknown error occurred.';
            }
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = errorMessage;
            errorElement.style.display = 'block';
            return;
        }

        // Success - redirect to places list
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Error during place creation:', error);
        const errorElement = document.getElementById('error-message');
        errorElement.textContent = 'An error occurred while creating the place. Please try again.';
        errorElement.style.display = 'block';
    }
}
