CREATE DATABASE IF NOT EXISTS mvc_db;
USE mvc_db;

CREATE TABLE club_location (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('Head', 'Branch') NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    web_address VARCHAR(200),
    max_capacity INT UNSIGNED NOT NULL
);

CREATE TABLE club_hobby (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE club_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    sender VARCHAR(255) NOT NULL,
    receiver VARCHAR(254) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body_snippet TEXT
);

CREATE TABLE club_personnel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    social_security_number VARCHAR(20) UNIQUE NOT NULL,
    medicare_card_number VARCHAR(20) UNIQUE NOT NULL,
    telephone_number VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    email_address VARCHAR(254) UNIQUE NOT NULL
);

CREATE TABLE club_personnelassignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    personnel_id INT NOT NULL,
    location_id INT NOT NULL,
    role ENUM('Administrator', 'General Manager', 'Deputy Manager', 'Treasurer', 'Secretary', 'Captain', 'Coach', 'Assistant Coach', 'Other') NOT NULL,
    mandate ENUM('Volunteer', 'Salaried') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    FOREIGN KEY (personnel_id)
        REFERENCES club_personnel (id)
        ON DELETE CASCADE,
    FOREIGN KEY (location_id)
        REFERENCES club_location (id)
        ON DELETE CASCADE,
    CONSTRAINT valid_date_range CHECK (end_date IS NULL
        OR end_date >= start_date),
    UNIQUE KEY unique_personnel_start_date (personnel_id , start_date)
);

CREATE TABLE club_familymember (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    social_security_number VARCHAR(20) UNIQUE NOT NULL,
    medicare_card_number VARCHAR(20) UNIQUE NOT NULL,
    telephone_number VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    email_address VARCHAR(254) UNIQUE NOT NULL,
    location_id INT NULL,
    FOREIGN KEY (location_id)
        REFERENCES club_location (id)
        ON DELETE SET NULL
);

CREATE TABLE club_secondaryfamilymember (
    id INT AUTO_INCREMENT PRIMARY KEY,
    primary_family_member_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    telephone_number VARCHAR(20) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    FOREIGN KEY (primary_family_member_id)
        REFERENCES club_familymember (id)
        ON DELETE CASCADE
);

CREATE TABLE club_clubmember (
    id INT AUTO_INCREMENT PRIMARY KEY,
    membership_number CHAR(36) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    social_security_number VARCHAR(20) UNIQUE NOT NULL,
    medicare_card_number VARCHAR(20) UNIQUE NOT NULL,
    telephone_number VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    email_address VARCHAR(254) UNIQUE NOT NULL,
    height DECIMAL(5,2) NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    location_id INT NULL,
    date_joined DATE DEFAULT (CURRENT_DATE),
    gender ENUM('M', 'F') DEFAULT 'M',
    FOREIGN KEY (location_id) REFERENCES club_location(id) ON DELETE SET NULL
);

CREATE TABLE club_clubmember_hobbies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clubmember_id INT NOT NULL,
    hobby_id INT NOT NULL,
    FOREIGN KEY (clubmember_id)
        REFERENCES club_clubmember (id)
        ON DELETE CASCADE,
    FOREIGN KEY (hobby_id)
        REFERENCES club_hobby (id)
        ON DELETE CASCADE,
    UNIQUE KEY unique_member_hobby (clubmember_id , hobby_id)
);

CREATE TABLE club_minormemberassociation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    minor_member_id INT NOT NULL,
    relationship ENUM('Father', 'Mother', 'Grand-father', 'Grand-mother', 'Tutor', 'Partner', 'Friend', 'Other') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    FOREIGN KEY (minor_member_id)
        REFERENCES club_clubmember (id)
        ON DELETE CASCADE,
    FOREIGN KEY (family_member_id)
        REFERENCES club_familymember (id)
        ON DELETE CASCADE,
    UNIQUE KEY unique_minor_start_date (minor_member_id , start_date)
);
CREATE TABLE club_payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_member_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10 , 2 ) NOT NULL,
    method_of_payment ENUM('Cash', 'Debit', 'Credit') NOT NULL,
    for_year INT UNSIGNED NOT NULL,
    FOREIGN KEY (club_member_id)
        REFERENCES club_clubmember (id)
        ON DELETE CASCADE
);

CREATE TABLE club_teamformation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    head_coach_id INT NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    is_game BOOLEAN DEFAULT FALSE,
    score_team1 INT UNSIGNED NULL,
    score_team2 INT UNSIGNED NULL,
    FOREIGN KEY (location_id)
        REFERENCES club_location (id)
        ON DELETE CASCADE,
    FOREIGN KEY (head_coach_id)
        REFERENCES club_personnel (id)
        ON DELETE CASCADE
);

CREATE TABLE club_playerassignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_member_id INT NOT NULL,
    team_formation_id INT NOT NULL,
    role ENUM('Setter', 'Outside hitter', 'Opposite hitter', 'Middle blocker', 'Defensive specialist', 'Libero') NOT NULL,
    FOREIGN KEY (club_member_id)
        REFERENCES club_clubmember (id)
        ON DELETE CASCADE,
    FOREIGN KEY (team_formation_id)
        REFERENCES club_teamformation (id)
        ON DELETE CASCADE,
    UNIQUE KEY unique_member_formation (club_member_id , team_formation_id)
);

-- trigger to prevent overlapping personnel assignments
CREATE TRIGGER enforce_no_overlap_personnel_bcnf
    BEFORE INSERT ON club_personnelassignment
    FOR EACH ROW
BEGIN
    DECLARE overlap_count INT DEFAULT 0;

SELECT
    COUNT(*)
INTO overlap_count FROM
    club_personnelassignment
WHERE
    personnel_id = NEW.personnel_id
        AND ((NEW.start_date BETWEEN start_date AND COALESCE(end_date, '9999-12-31'))
        OR (COALESCE(NEW.end_date, '9999-12-31') BETWEEN start_date AND COALESCE(end_date, '9999-12-31'))
        OR (NEW.start_date <= start_date
        AND COALESCE(NEW.end_date, '9999-12-31') >= COALESCE(end_date, '9999-12-31')));

    IF overlap_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Personnel cannot have overlapping assignments';
    END IF;
END$$

DELIMITER ;
