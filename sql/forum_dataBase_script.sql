-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema forum_database1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum_database1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_database1` DEFAULT CHARACTER SET latin1 ;
USE `forum_database1` ;

-- -----------------------------------------------------
-- Table `forum_database1`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_database1`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_database1`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_database1`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idusers_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_database1`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_database1`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `message_text` TEXT NOT NULL,
  `sender_id` INT(11) NOT NULL,
  `recipient_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_message_users1_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users1_idx` (`recipient_id` ASC) VISIBLE,
  CONSTRAINT `fk_message_users1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_database1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`recipient_id`)
    REFERENCES `forum_database1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_database1`.`permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_database1`.`permissions` (
  `users_id` INT(11) NOT NULL,
  `categories_id` INT(11) NOT NULL,
  PRIMARY KEY (`users_id`, `categories_id`),
  INDEX `fk_permissions_categories1_idx` (`categories_id` ASC) VISIBLE,
  CONSTRAINT `fk_permissions_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forum_database1`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_permissions_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_database1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_database1`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_database1`.`topics` (
  `id` INT(11) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `categories_id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_topics_categories_idx` (`categories_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forum_database1`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_database1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_database1`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_database1`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `topics_id` INT(11) NOT NULL,
  `description` TEXT NOT NULL,
  `users_id` INT(11) NOT NULL,
  `topics_id1` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_replies_topics1_idx` (`topics_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_replies_topics2_idx` (`topics_id1` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topics_id`)
    REFERENCES `forum_database1`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_topics2`
    FOREIGN KEY (`topics_id1`)
    REFERENCES `forum_database1`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_database1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_database1`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_database1`.`votes` (
  `type` TINYINT(4) NULL DEFAULT NULL,
  `users_id` INT(11) NOT NULL,
  `replies_id` INT(11) NOT NULL,
  PRIMARY KEY (`users_id`, `replies_id`),
  INDEX `fk_Votes_replies1_idx` (`replies_id` ASC) VISIBLE,
  CONSTRAINT `fk_Votes_replies1`
    FOREIGN KEY (`replies_id`)
    REFERENCES `forum_database1`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Votes_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_database1`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;