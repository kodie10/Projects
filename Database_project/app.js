//Citation for the following page
//Date: 11/2/2022
//Adapted From:
//Source URL: https://github.com/osu-cs340-ecampus/nodejs-starter-app

/*
    SETUP
*/
var express = require('express');
var app = express(); 
PORT = 7846; 

const {
    engine
} = require('express-handlebars');
var exphbs = require('express-handlebars'); 
const { NULL } = require('mysql/lib/protocol/constants/types');
app.engine('.hbs', engine({
    extname: ".hbs"
})); 
app.set('view engine', '.hbs'); 

// Database
var db = require('./database/db-connector')

app.use(express.json())
app.use(express.urlencoded({
    extended: true
}))
//app.use(express.static('public'))
app.use(express.static(__dirname + '/public')); 
/*
    ROUTES
*/
//homepage
app.get('/', function (req, res) {
    return res.render('index.hbs')
});

//display data for Pokemon page queries for dropdowns
app.get('/pokemon.hbs', function (req, res) {
    // SQL query to SELECT data we want to show on the page
    let query1 = `SELECT Pokemon.pokemon_id, Pokemon.name, Pokemon.nickname, Pokemon.level, Trainers.trainer_id, Trainers.f_name, Trainers.l_name, Types.name AS 'type'
    FROM Pokemon
    LEFT JOIN Trainers on Trainers.trainer_id = Pokemon.trainer_id
    INNER JOIN Types on Types.type_id = Pokemon.type_id;`
    // query for dropdown
    let query2 = `SELECT Pokemon.pokemon_id, Pokemon.name FROM Pokemon;`;
    // query for second dropdown
    let query3 = `SELECT Trainers.trainer_id, Trainers.f_name, Trainers.l_name FROM Trainers;`
    // query for third dropdown
    let query4 = `SELECT Types.type_id, Types.name AS 'type' FROM Types;`

    db.pool.query(query1, function (error, rows, fields) {
        // save pokemon
        let pokemon_id = rows;
        db.pool.query(query2, (error, rows, fields) => {
            // save name
            let name = rows;

            db.pool.query(query3, (error, rows, fields) => {
                // save trainer
                let trainers = rows;

                db.pool.query(query4, (error, rows, fields) => {
                    // save type
                    let type = rows;

                    return res.render('pokemon', { data: pokemon_id, name: name, trainers: trainers, type: type});
                })
            })
        })
    })
});

//route and code for adding pokemon to database
app.post('/add-pokemon-form', function (req, res) {
    // data to insert into database
    let data = req.body;
    let nickname = data['input-pokemon-nickname']
    let trainer = parseInt(data['input-pokemon-trainer'])
    let type = parseInt(data['input-pokemon-type'])
    // query to INSERT pokemon entered by user
    query1 = `INSERT INTO Pokemon (name, nickname, trainer_id, type_id, level) VALUES ('${data['input-pokemon-name']}', '${nickname}', '${trainer}', '${type}', '${data['input-pokemon-level']}')`;
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error)
            res.sendStatus(400);
        }

        else {
            res.redirect('/pokemon.hbs');
        }
    })
});

// route and code for updating pokemon in database
app.post('/update-pokemon-form', function (req, res, next) {
    // data to update database
    let data = req.body;
    let level = parseInt(data['input-level-update']);
    let nickname = data['input-nickname-update'];
    let trainer_id = parseInt(data['input-trainer-update']);
    if (isNaN(trainer_id)){
        trainer_id = 'null'
    }
    // query to UPDATE Pokemon selected by user 
    let queryUpdatePokemon = `UPDATE Pokemon SET Pokemon.nickname = "${nickname}", Pokemon.trainer_id = ${trainer_id}, Pokemon.type_id = ('${data['input-type-update']}'), Pokemon.level = '${level}' WHERE Pokemon.pokemon_id = ('${data['input-pokemon-update']}')`;

    db.pool.query(queryUpdatePokemon, function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.redirect('/pokemon.hbs')
        }
    })
});

// route and code for deleting pokemon received from user from database
app.delete('/delete-pokemon-ajax/', function (req, res, next) {
    // data to delete Pokemon
    let data = req.body;
    let pokemonId = parseInt(data.pokemon_id);
    // query to DELETE Pokemon selected by user
    let deletePokemon = `DELETE FROM Pokemon WHERE pokemon_id = ?`;
        
        db.pool.query(deletePokemon, [pokemonId], function (error, rows, fields) {
            if (error) {
                
                console.log(error);
                res.sendStatus(400);
            } 
            
            else {
                res.sendStatus(204);
            }
        })
});

//display data for Trainers page and display for search function
app.get('/trainers.hbs', function (req, res) {
    let query1;
    // SELECT all from trainers if nothing is in the search
    if (req.query.l_name === undefined) {
        query1 = "SELECT * FROM Trainers;";
    }
    // or SELECT all from trainers if something is entered in search box
    else {
        query1 = `SELECT * FROM Trainers WHERE l_name LIKE "${req.query.l_name}%"`
    }

    db.pool.query(query1, function (error, rows, fields) {

        // Save the trainers
        let trainers = rows;

        return res.render('trainers', { data: trainers });
    })
});

// route and code to add trainers to the database
app.post('/add-trainers-form', function (req, res) {
    let data = req.body;
    // SQL to insert data from user
    query1 = `INSERT INTO Trainers (f_name, l_name, hometown) VALUES ('${data['input-f_name']}', '${data['input-l_name']}', '${data['input-hometown']}')`;
    
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error)
            res.sendStatus(400);
        }

        else {
            res.redirect('/trainers.hbs');
        }
    })
});

// route and code to delete a trainer
app.delete('/delete-trainers-ajax/', function (req, res, next) {
    // data selected by user to delete
    let data = req.body;
    let trainerId = parseInt(data.trainer_id);
    // query to DELETE trainer selected by user
    let deleteTrainer = `DELETE FROM Trainers WHERE trainer_id = ?`;

    db.pool.query(deleteTrainer, [trainerId], function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.sendStatus(204);
        }
    })
});

// route and code to display attacks page
app.get('/attacks.hbs', function (req, res) {
    // SELECT query to display data from attacks on the page
    let query1 = `SELECT Attacks.attack_id, Attacks.name, Attacks.atk_power, Attacks.power_points, Types.name AS 'type'
                  FROM Attacks
                  INNER JOIN Types ON Types.type_id = Attacks.type_id;`
    // SELECT query for dropdown
    let query2 = `SELECT Types.type_id, Types.name AS 'type' FROM Types;`
    // SELECT query for second dropdown
    let query3 = `SELECT Attacks.attack_id, Attacks.name AS 'atkname' FROM Attacks;`

    db.pool.query(query1, function (error, rows, fields) {
        // save attack_id
        let attack_id = rows;

        db.pool.query(query2, (error, rows, fields) => {
            // save type
            let type = rows;

            db.pool.query(query3, (error, rows, fields) => {
                // save atkname
                let atkname = rows;

            return res.render('attacks', { data: attack_id, type: type, atkname: atkname });
            })
        })
    })
});

// route and code to add attack
app.post('/add-attacks-form', function (req, res) {
    // data entered by user
    let data = req.body;
    let type = parseInt(data['input-attack-type'])
    // SQL query to INSERT data from user into database
    query1 = `INSERT INTO Attacks (name, atk_power, power_points, type_id) VALUES ('${data['input-attack-name']}', '${data['input-atk_power']}', '${data['input-power_points']}', '${type}')`;
    
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error)
            res.sendStatus(400);
        }

        else {
            res.redirect('/attacks.hbs');
        }
    })
});

// route and code to update attacks
app.post('/update-attacks-form', function (req, res, next) {
    // data entered by user to update
    let data = req.body;
    // SQL query to UPDATE attack selected by user with data from user
    let queryUpdateAttack = `UPDATE Attacks SET Attacks.atk_power = ('${data['input-atk_power-update']}'), Attacks.power_points = ('${data['input-power_points-update']}') WHERE Attacks.attack_id = ('${data['input-attack-update']}')`;

    db.pool.query(queryUpdateAttack, function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.redirect('/attacks.hbs')
        }
    })
});

// route and code to delete attack
app.delete('/delete-attacks-ajax/', function (req, res, next) {
    // data selected by user
    let data = req.body;
    let attackID = parseInt(data.attack_id);
    // SQL query to delete attack selected from user
    let deleteAttack = `DELETE FROM Attacks WHERE attack_id = ?`;

    db.pool.query(deleteAttack, [attackID], function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.sendStatus(204);
        }
    })
});

// route and code to display type page
app.get('/types.hbs', function (req, res) { 
    // SQL to display on page
    let query1 = `SELECT * From Types;`
    // SQL for dropdown
    let query2 = `SELECT Types.type_id, Types.name AS 'type' FROM Types;`

    db.pool.query(query1, function (error, rows, fields) {
        // save type_id
        let type_id = rows;

        db.pool.query(query2, (error, rows, fields) => {
            // save type
            let type = rows;

        return res.render('types', { data: type_id, type: type});
        })
    })
});

// route and code to add types
app.post('/add-types-form', function (req, res) {
    // data entered by user
    let data = req.body;
    // SQL to INSERT type entered by user
    query1 = `INSERT INTO Types (name, super_effective, weakness, no_effect) VALUES ('${data['input-type-name']}', '${data['input-super_effective']}', '${data['input-weakness']}', '${data['input-no_effect']}')`;
    
    db.pool.query(query1, function (error, rows, fields) {
        if (error) {

            console.log(error)
            res.sendStatus(400);
        }

        else {
            res.redirect('/types.hbs');
        }
    })
});

// route and code to update type
app.post('/update-type-form', function (req, res, next) {
    // data entered by user
    let data = req.body;
    let no_effect = data['input-no_effect-update'];
    // handles if entry is blank
    if (no_effect === ''){
        no_effect = 'NULL'
    }
    // SQL to UPDATE types from data entered by user
    let queryUpdateType = `UPDATE Types SET Types.super_effective = ('${data['input-super_effective-update']}'), Types.weakness = ('${data['input-weakness-update']}'), Types.no_effect =  '${no_effect}' WHERE Types.type_id = ('${data['input-type-update']}')`;

    db.pool.query(queryUpdateType, function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.redirect('/types.hbs')
        }
    })
});

// route and code to delete types
app.delete('/delete-types-ajax/', function (req, res, next) {
    // data entered by user
    let data = req.body;
    let typeID = parseInt(data.type_id);
    // SQL to DELETE type selected by user
    let deleteType = `DELETE FROM Types WHERE type_id = ?`;

    db.pool.query(deleteType, [typeID], function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.sendStatus(204);
        }
    })
});

// route and code to display data for the Learned_Attacks page
app.get('/Learned_Attacks.hbs', function (req, res) {
    // query to display data on page
    let query1 = `SELECT Learned_Attacks.learned_attacks_id, Pokemon.pokemon_id, Pokemon.name, Attacks.name AS 'atkname', Attacks.attack_id
                  FROM Learned_Attacks
                  INNER JOIN Pokemon ON Pokemon.pokemon_id = Learned_Attacks.pokemon_id
                  INNER JOIN Attacks ON Attacks.attack_id = Learned_Attacks.attack_id;`;
    // query for dropdown              
    let query2 = `SELECT Pokemon.pokemon_id, Pokemon.name FROM Pokemon`
    // query for second dropdown
    let query3 = `SELECT Attacks.attack_id, Attacks.name AS 'atkname' FROM Attacks;`
    // query for third dropdown
    let query4= `SELECT Learned_Attacks.learned_attacks_id, Pokemon.pokemon_id, Pokemon.name 
                 FROM Learned_Attacks
                 INNER JOIN Pokemon ON Pokemon.pokemon_id = Learned_Attacks.pokemon_id;`;

    db.pool.query(query1, function (error, rows, fields) {
        // save pokemon_id
        let pokemon_id = rows;

        db.pool.query(query2, (error, rows, fields) => {
            // save name
            let name = rows;

            db.pool.query(query3, (error, rows, fields) => {
                // save atkname
                let atkname = rows;

                db.pool.query(query4, (error, rows, fields) => {
                    // save learned_attacks_id
                    let learned_attacks_id= rows;

                    return res.render('Learned_Attacks', { data: pokemon_id, name: name, atkname: atkname, learned_attacks_id:learned_attacks_id });
                })
            });
        })
    })
});

// route and code to add learned attack
app.post('/add-Learned_Attack-form', function (req, res) {
    // data entered by user
    let data = req.body;
    // SQL to INSERT data from user 
    query1 = `INSERT INTO Learned_Attacks (pokemon_id, attack_id) VALUES ('${data['input-pokemonla']}', '${data['input-attackla']}')`;

    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error)
            res.sendStatus(400);
        }

        else {
            res.redirect('/Learned_Attacks.hbs');
        }

    })
});

// route and code to update Learned Attacks
app.post('/update-la-form', function (req, res, next) {
    // data selected from user
    let data = req.body;
    // SQL query to UPDATE with data selected from user
    let query1 = `UPDATE Learned_Attacks SET Learned_Attacks.attack_id = ('${data['input-attack-update']}') WHERE Learned_Attacks.learned_attacks_id = ('${data['input-pokemonula-update']}')`;

    db.pool.query(query1, function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.redirect('/learned_attacks.hbs')
        }
    })
});

// route and code to delete a Learned Attack
app.delete('/delete-Learned_Attack-ajax/', function (req, res, next) {
    // data selected by user
    let data = req.body;
    let learnedAttacksId = parseInt(data.learned_attacks_id);
    // SQL to DELETE a learned attack selected by user
    let deleteLearnedAttack = `DELETE FROM Learned_Attacks WHERE Learned_Attacks.learned_attacks_id =?`;

    db.pool.query(deleteLearnedAttack, [learnedAttacksId], function (error, rows, fields) {
        if (error) {

            console.log(error);
            res.sendStatus(400);
        }

        else {
            res.sendStatus(204);
        }
    })
});

/*
    LISTENER
*/

app.listen(PORT, function () {       
    console.log('Express started on http://localhost:' + PORT + '; press Ctrl-C to terminate.')
});