
-- -----------------------------------------------------
-- Table `Trainers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Trainers` (
  `trainer_id` INT AUTO_INCREMENT,
  `f_name` VARCHAR(45) NOT NULL,
  `l_name` VARCHAR(45) NOT NULL,
  `hometown` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`trainer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Types` (
  `type_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `super_effective` VARCHAR(45) NULL,
  `weakness` VARCHAR(45) NULL,
  `no_effect` VARCHAR(45) NULL,
  PRIMARY KEY (`type_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Pokemon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Pokemon` (
  `pokemon_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `nickname` VARCHAR(45),
  `trainer_id` INT,
  `type_id` INT NOT NULL,
  `level` INT NOT NULL,
  PRIMARY KEY (`pokemon_id`),
    FOREIGN KEY (`trainer_id`)
    REFERENCES `Trainers` (`trainer_id`)
    ON DELETE SET NULL,
    FOREIGN KEY (`type_id`)
    REFERENCES `Types` (`type_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Attacks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Attacks` (
  `attack_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL UNIQUE,
  `atk_power` INT NOT NULL,
  `power_points` INT NOT NULL,
  `type_id` INT NOT NULL,
  PRIMARY KEY (`attack_id`),
    FOREIGN KEY (`type_id`)
    REFERENCES `Types` (`type_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Learned_Attacks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Learned_Attacks` (
  `learned_attacks_id` INT NOT NULL AUTO_INCREMENT,
  `pokemon_id` INT NOT NULL,
  `attack_id` INT NOT NULL,
  PRIMARY KEY (`learned_attacks_id`),
    FOREIGN KEY (`pokemon_id`)
    REFERENCES `Pokemon` (`pokemon_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`attack_id`)
    REFERENCES `Attacks` (`attack_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

INSERT INTO `Trainers` (`f_name`, `l_name`, `hometown`)
VALUES ('Ash', 'Ketchum', 'Pallet Town'),
('Gary', 'Rival', 'Pallet Town'),
('Kodie', 'Artmayer', 'Cincinnati');

INSERT INTO `Types` (`name`, `super_effective`, `weakness`, `no_effect`)
VALUES ('grass', 'rock', 'fire', NULL),
('water', 'fire', 'electric', NULL),
('fire', 'grass', 'water', NULL),
('electric', 'water', 'rock', NULL),
('rock', 'water', 'electric', NULL);

INSERT INTO `Pokemon` (`name`, `nickname`, `trainer_id`, `type_id`, `level`)
VALUES ('Bulbasaur', NULL, (SELECT Trainers.trainer_id FROM Trainers WHERE Trainers.f_name = 'Ash' and Trainers.l_name = 'Ketchum'), (SELECT Types.type_id From Types WHERE Types.name = 'grass'), 6),
('Squirtle', NULL, (SELECT Trainers.trainer_id FROM Trainers WHERE Trainers.f_name = 'Gary' and Trainers.l_name = 'Rival'), (SELECT Types.type_id From Types WHERE Types.name = 'grass'), 6), 
('Pikachu', 'Sparky', (SELECT Trainers.trainer_id FROM Trainers WHERE Trainers.f_name = 'Kodie' and Trainers.l_name = 'Artmayer'), (SELECT Types.type_id From Types WHERE Types.name = 'electric'), 6),
('Pikachu', NULL, (SELECT Trainers.trainer_id FROM Trainers WHERE Trainers.f_name = 'Ash' and Trainers.l_name = 'Ketchum'), (SELECT Types.type_id From Types WHERE Types.name = 'electric'), 10);

INSERT INTO `Attacks` (`name`, `atk_power`, `power_points`, `type_id`)
VALUES ('vine whip', 45, 25, (SELECT Types.type_id FROM Types WHERE Types.name = 'grass')),
('thundershock', 55, 25, (SELECT Types.type_id From Types WHERE Types.name = 'electric')),
('thunderbolt', 80, 15, (SELECT Types.type_id From Types WHERE Types.name = 'electric')),
('bubble', 30, 35, (SELECT Types.type_id From Types WHERE Types.name = 'water'));

INSERT INTO `Learned_Attacks` (`pokemon_id`, `attack_id`)
VALUES ((SELECT Pokemon.pokemon_id FROM Pokemon WHERE Pokemon.name = 'Pikachu' and Pokemon.trainer_id = 1), (SELECT Attacks.attack_id FROM Attacks WHERE Attacks.name = 'thundershock')),
((SELECT Pokemon.pokemon_id FROM Pokemon WHERE Pokemon.name = 'Pikachu' and Pokemon.trainer_id = 3), (SELECT Attacks.attack_id FROM Attacks WHERE Attacks.name = 'thunderbolt')),
((SELECT Pokemon.pokemon_id FROM Pokemon WHERE Pokemon.name = 'Squirtle' and Pokemon.trainer_id = 2), (SELECT Attacks.attack_id FROM Attacks WHERE Attacks.name = 'bubble')),
((SELECT Pokemon.pokemon_id FROM Pokemon WHERE Pokemon.name = 'Bulbasaur' and Pokemon.trainer_id = 1), (SELECT Attacks.attack_id FROM Attacks WHERE Attacks.name = 'vine whip'));

