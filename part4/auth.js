// auth.js
document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------
    // Utility Function: Get Cookie by Name
    // -------------------------------------
    const getCookie = (name) => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) {
        return parts.pop().split(';').shift();
      }
      return null;
    };
  
    // -----------------------------------------------------------
    // Toggle Login/Logout Buttons Based on Authentication Status
    // -----------------------------------------------------------
    const loginLink = document.getElementById('auth-link');    // Login button element
    const logoutLink = document.getElementById('logout-link');   // Logout button element
    const token = getCookie('token');
    console.log('Token found:', token); // Debug logging
  
    if (token) {
      // User is authenticated: hide the login button, show the logout button.
      if (loginLink) loginLink.style.display = 'none';
      if (logoutLink) logoutLink.style.display = 'block';
    } else {
      // User is not authenticated: show the login button, hide the logout button.
      if (loginLink) loginLink.style.display = 'block';
      if (logoutLink) logoutLink.style.display = 'none';
    }
  
    // -----------------------------------------------------------
    // Login Form Submission (for login.html)
    // -----------------------------------------------------------
    const loginForm = document.getElementById('login-form');
    const errorMessageDiv = document.getElementById('error-message');
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission
  
        // Get credentials from form fields.
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
  
        // Clear previous error messages.
        if (errorMessageDiv) {
          errorMessageDiv.style.display = 'none';
          errorMessageDiv.textContent = '';
        }
  
        try {
          const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
          });
  
          if (response.ok) {
            const data = await response.json();
            // Store the JWT token in a cookie.
            document.cookie = `token=${data.access_token}; path=/; SameSite=Strict`;
            // Redirect the user to the main page.
            window.location.href = 'index.html';
          } else {
            // Display an error message if login fails.
            const errorData = await response.json();
            if (errorMessageDiv) {
              errorMessageDiv.textContent = errorData.message || 'Login failed. Please check your credentials.';
              errorMessageDiv.style.display = 'block';
            }
          }
        } catch (error) {
          if (errorMessageDiv) {
            errorMessageDiv.textContent = 'An error occurred. Please try again later.';
            errorMessageDiv.style.display = 'block';
          }
          console.error('Login error:', error);
        }
      });
    }
  
    // -----------------------------------------------------------
    // Logout Functionality
    // -----------------------------------------------------------
    if (logoutLink) {
      logoutLink.addEventListener('click', (event) => {
        event.preventDefault();
        // Clear the JWT token cookie.
        document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
        // Redirect the user to the login page.
        window.location.href = 'login.html';
      });
    }
  });
  