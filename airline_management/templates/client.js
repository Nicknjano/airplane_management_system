document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Log server response for debugging

        if (data.message === 'Login successful') {
            // Redirect to dashboard or home page on successful login
            window.location.href = 'home.html'; 
        } else {
            // Display error message for invalid credentials
            alert('Invalid email or password. Please try again.');
        }
    })
    .catch(error => {
        console.error('There was a problem with the login request:', error);
        // Display error message for network or server errors
        alert('An error occurred while logging in. Please try again later.');
    });
});
