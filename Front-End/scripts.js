document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

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
});

async function loginUser(email, password) {
    try {
        console.log('Attempting login with email:', email);
        const response = await fetch('http://127.0.0.1:5001/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        
        if (response.ok) {
            console.log('Login successful, setting token');
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            console.error('Login failed:', data.error);
            const errorMessage = document.getElementById('error-message');
            if (errorMessage) {
                errorMessage.textContent = data.error || 'Invalid email or password';
                errorMessage.style.display = 'block';
            } else {
                console.error('Error message element not found');
            }
        }
    } catch (error) {
        console.error('Login error:', error);
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
            errorMessage.textContent = 'An error occurred. Please try again.';
            errorMessage.style.display = 'block';
        } else {
            console.error('Error message element not found');
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
