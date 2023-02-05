//Citation for the following page
//Date: 11/2/2022
//Copied From:
//Source URL: https://github.com/osu-cs340-ecampus/nodejs-starter-app

// ./database/db-connector.js

// Get an instance of mysql we can use in the app
var mysql = require('mysql')

// Create a 'connection pool' using the provided credentials
var pool = mysql.createPool({
    connectionLimit : 10,
    host            : 'classmysql.engr.oregonstate.edu',
    user            : 'cs340_artmayek',
    password        : '8622',
    database        : 'cs340_artmayek'
})

// Export it for use in our applicaiton
module.exports.pool = pool;