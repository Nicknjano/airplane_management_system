// server.js

// Import required modules
const express = require('express');
const sqlite3 = require('sqlite3').verbose();

// Initialize Express app
const app = express();
const port = 3000;

// Connect to SQLite database
const db = new sqlite3.Database('database.sqlite');

// Define endpoint to fetch users
app.get('/users', (req, res) => {
    // Query the database to fetch users
    db.all('SELECT * FROM users', (err, rows) => {
        if (err) {
            console.error(err.message);
            return res.status(500).json({ error: 'Internal server error' });
        }
        // Send user data as JSON response
        res.json(rows);
    });
});

// Start server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
