-- Get all Trainers and their information for the Trainers page
SELECT * FROM Trainers;
-- Search for a specific trainer by last name
select * from Trainers
WHERE Trainers.l_name = `:l_name_input_from_user_search`;
-- Add a new Trainer
INSERT INTO `Trainers` (`f_name`, `l_name`, `hometown`)
VALUES (`:f_name_input`, `:l_name_input`, `:hometown_input`);
-- Delete a Trainer
DELETE FROM Trainers WHERE `trainer_id` = `:trainer_id_selected_from_Trainers_page`;

-- Get all Pokemon and their information and the Trainer they belong to for the Pokemon Page
select Pokemon.pokemon_id, Pokemon.name, Pokemon.nickname, Pokemon.level, Trainers.f_name AS 'first name', Trainers.l_name AS 'last name', Types.name AS 'Type'
from Pokemon
inner join Trainers on Trainers.trainer_id = Pokemon.trainer_id
inner join Types on Types.type_id = Pokemon.type_id;
-- Get Trainers for Trainer dropdown
SELECT Trainers.trainer_id, Trainers.f_name, Trainers.l_name
FROM Trainers;
-- Get Types for Types dropdown
SELECT Types.type_id, Types.name
FROM Types;
-- Add a new Pokemon
INSERT INTO `Pokemon` (`name`, `nickname`, `trainer_id`, `type_id`, `level`)
VALUES (`:name_input`, `:nickname_input`, `:trainer_id_from_dropdown`, `:type_id_from_dropdown`, `:level_input`);
-- Delete a Pokemon
DELETE FROM Pokemon WHERE Pokemon.pokemon_id = `:pokemon_id_selected_from_Pokemon_page`;
-- Update Pokemon information
SELECT Pokemon.pokemon_id, Pokemon.nickname, Pokemon.trainer_id, Pokemon.level
FROM Pokemon
WHERE Pokemon.pokemon_id = `:pokemon_id_selected_from_Pokemon_page`;
UPDATE Pokemon
SET `nickname` = `:nickname_input`, `trainer_id` = `:trainer_id_input`, `level` = `:level_input`
WHERE Pokemon.pokemon_id = `:pokemon_id_selected_from_Pokemon_page`;

-- Get all Types and their information for the Types Page
SELECT * From Types;
-- Add a new Type
INSERT INTO `Types` (`name`, `super_effective`, `weakness`, `no_effect`)
VALUES (`:name_input`, `:super_effective_input`, `:weakness_input`, `:no_effect_input`);
-- Delete a Type 
DELETE FROM Types WHERE Types.type_id = `:type_id_selected_from_Types_page`;
-- Update Types information
SELECT Types.type_id, Types.super_effective, Types.weakness, Types.no_effect
FROM Types
WHERE Types.type_id = `type_id_selected_from_Types_page`;
UPDATE Types
SET `super_effective` = `:super_effective_input`, `weakness` = `:weakness_input`, `no_effect` = `no_effect_input`
WHERE Types.type_id = `type_id_selected_from_Types_page`;

-- Get all Attacks and their information for the Attacks Page
SELECT Attacks.attack_id, Attacks.name, Attacks.atk_power AS 'attack power', Attacks.power_points AS 'power points', Types.name AS type
FROM Attacks
INNER JOIN Types ON Types.type_id = Attacks.attack_id;
-- Add a new attack
INSERT INTO `Attacks` (`name`, `atk_power`, `power_points`, `type_id`)
VALUES (`:name_input`, `:atk_power_input`, `:power_points_input`, `:type_id_from_dropdown`);
-- Delete an attack
DELETE FROM Attacks WHERE Attack.attack_id = `:attack_id_selected_from_Attacks_page`;
-- Update an attack information
SELECT Attacks.atk_power, Attacks.power_points
FROM Attacks
WHERE Attacks.attack_id = `:attack_id_selected_from_Attacks_page`;
UPDATE Attacks
SET `atk_power` = `:atk_power_input`, `power_points` = `:power_points_input`
WHERE Attacks.attack_id = `:attack_id_selected_from_Attacks_page`;

-- Get all Attacks that are learned by a Pokemon for the Learned_Attacks Page
SELECT Pokemon.pokemon_id, Pokemon.name, Attacks.name AS 'attack name'
FROM Learned_Attacks
INNER JOIN Pokemon ON Pokemon.pokemon_id = Learned_Attacks.pokemon_id
INNER JOIN Attacks ON Attacks.attack_id = Learned_Attacks.attack_id; 
-- Get Attacks for an attack dropdown
SELECT Attacks.attack_id, Attacks.name
FROM Attacks;
-- Get Pokemon for a Pokemon dropdown
SELECT Pokemon.Pokemon_id, Pokemon.name
FROM Pokemon;
-- Associate an attack with a Pokemon (M:N relationship addition)
INSERT INTO `Learned_Attacks` (`pokemon_id`, `attack_id`)
VALUES (`:pokemon_id_from_dropdown`, `:attack_id_from_dropdown`);
-- Dis-associate an attack from a Pokemon (M:N relationship deletion)
DELETE FROM Learned_Attacks
WHERE Learned_Attacks.pokemon_id = `:pokemon_id_selected_from_Learned_Attacks_page` 
AND Learned_Attacks.attack_id = `:attack_id_selected_from_Learned_Attacks_page`;
-- Update the Relationship between Pokemon and Attacks
SELECT Learned_Attacks.pokemon_id, Learned_Attacks.attack_id
FROM Learned_Attacks;
UPDATE Learned_Attacks
SET `pokemon_id` = `:pokemon_id_from_dropdown`, `attack_id` = `:attack_id_from_dropdown`
WHERE Learned_Attacks.pokemon_id = `:pokemon_id_selected_from_Learned_Attacks_page` 
AND Learned_Attacks.attack_id = `:attack_id_selected_from_Learned_Attacks_page`;
