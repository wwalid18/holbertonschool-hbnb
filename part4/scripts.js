// part4/scripts.js

document.addEventListener('DOMContentLoaded', () => {
  // Function to get a cookie by name
  const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
  };

  // Check if we're on index.html and update the auth link
  const authLink = document.getElementById('auth-link');
  if (authLink) {
      const token = getCookie('token');
      if (token) {
          // User is logged in
          authLink.textContent = 'Logout';
          authLink.href = '#'; // Prevent default navigation
          authLink.addEventListener('click', (event) => {
              event.preventDefault();
              // Clear the token cookie by setting its expiration to a past date
              document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
              // Redirect to login.html
              window.location.href = 'login.html';
          });
      } else {
          // User is not logged in
          authLink.textContent = 'Login';
          authLink.href = 'login.html';
      }
  }

  // Existing login form submission logic for login.html
  const loginForm = document.getElementById('login-form');
  const errorMessageDiv = document.getElementById('error-message');

  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault(); // Prevent default form submission

          // Get email and password from the form
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;

          // Clear any previous error messages
          errorMessageDiv.style.display = 'none';
          errorMessageDiv.textContent = '';

          try {
              // Make AJAX request to the login endpoint
              const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({ email, password })
              });

              // Handle the API response
              if (response.ok) {
                  const data = await response.json();
                  // Store the JWT token in a cookie
                  document.cookie = `token=${data.access_token}; path=/; SameSite=Strict`;
                  // Redirect to the main page
                  window.location.href = 'index.html';
              } else {
                  // Display error message if login fails
                  const errorData = await response.json();
                  errorMessageDiv.textContent = errorData.message || 'Login failed. Please check your credentials.';
                  errorMessageDiv.style.display = 'block';
              }
          } catch (error) {
              // Handle network or other errors
              errorMessageDiv.textContent = 'An error occurred. Please try again later.';
              errorMessageDiv.style.display = 'block';
              console.error('Login error:', error);
          }
      });
  }
});
