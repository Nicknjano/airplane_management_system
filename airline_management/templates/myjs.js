
	$(".nav li").on("click", function() {
      $(".nav li").removeClass("active");
      $(this).addClass("active");
    });



    function navbar_movment(event)
	{
        	$(event.data.param1).slideToggle("fast");
        /*	$(event.data.param2).slideUp("fast");
        	$(event.data.param3).slideUp("fast");
        	$(event.data.param4).slideUp("fast"); */
	};
// myjs.js

// Function to fetch users from the server and display them
function getUsers() {
    fetch('/users')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(users => {
        // Display users on the page
        const tableBody = document.getElementById('userTableBody');
        tableBody.innerHTML = ''; // Clear existing table content
        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.firstName}</td>
                <td>${user.lastName}</td>
                <td>${user.phone}</td>
                <td>${user.email}</td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('There was a problem fetching users:', error);
    });
}

// Call the getUsers function to fetch and display users when the page loads
document.addEventListener('DOMContentLoaded', getUsers);
