#/bin/bash

execute_query () {
	mysql -h $DB_HOST -u $DB_USER -p$DB_PASS -D klaudijus -e "$1"	 
}
#DROP TABLES
echo "Deleting tables ..."

execute_query 'DROP TABLE brew_order'
execute_query 'DROP TABLE round'
execute_query 'DROP TABLE person'
execute_query 'DROP TABLE drink'

#Recreate tables
echo "Creating tables..."

execute_query 'CREATE TABLE drink (drink_id INTEGER AUTO_INCREMENT PRIMARY KEY,display_name VARCHAR(100),drink_type VARCHAR(100),recipe VARCHAR(100))'

execute_query 'CREATE TABLE person (person_id INTEGER AUTO_INCREMENT PRIMARY KEY, display_name VARCHAR(100), name VARCHAR(100), team VARCHAR(100), favDrink_id INTEGER , FOREIGN KEY(favDrink_id) REFERENCES drink(drink_id) ON DELETE CASCADE)'

execute_query 'CREATE TABLE round (round_id INTEGER PRIMARY KEY AUTO_INCREMENT, initiator INTEGER, FOREIGN KEY(initiator) REFERENCES person(person_id))'

execute_query 'CREATE TABLE brew_order (order_id INTEGER PRIMARY KEY AUTO_INCREMENT, round_id INTEGER, person_id INTEGER, drink_id INTEGER, FOREIGN KEY(round_id) REFERENCES round(round_id), FOREIGN KEY(person_id) REFERENCES person(person_id), FOREIGN KEY(drink_id) REFERENCES drink(drink_id))'

#Insert Drinks
echo "Inserting Drinks"

execute_query 'INSERT INTO `drink`(display_name, drink_type, recipe) VALUES ("Coffee","coffee",NULL)'

execute_query 'INSERT INTO `drink`(display_name, drink_type, recipe) VALUES ("Water","cold",NULL)'

execute_query 'INSERT INTO `drink`(display_name, drink_type, recipe) VALUES ("Tea","hot",NULL)'

#Insert people
echo "Inserting People"

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id) VALUES ("Charlie", "charlie","Academy" , 1)'

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id) VALUES ("Henry", "henry","Academy" , 2)'

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id) VALUES ("David", "david","Academy" , 3)'

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id) VALUES ("Lindsay", "lindsay","Hermes" , 1)'

#Insert Rounds
echo "Inserting Rounds"

execute_query 'INSERT INTO `round`(initiator) VALUES (1)'
execute_query 'INSERT INTO `round`(initiator) VALUES (2)'
execute_query 'INSERT INTO `round`(initiator) VALUES (3)'
execute_query 'INSERT INTO `round`(initiator) VALUES (4)'
execute_query 'INSERT INTO `round`(initiator) VALUES (4)'
execute_query 'INSERT INTO `round`(initiator) VALUES (4)'
execute_query 'INSERT INTO `round`(initiator) VALUES (2)'

#Insert Orders

execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (1, 2, 2)'
execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (1, 3, 1)'

execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (2, 1, 3)'
execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (2, 3, 3)'

execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (3, 1, 2)'
execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (3, 2, 2)'

execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (4, 4, 2)'

execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (5, 4, 2)'

execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (6, 4, 2)'

execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (7, 1, 2)'
execute_query 'INSERT INTO `brew_order`(round_id, person_id, drink_id) VALUES (7, 3, 3)'


echo "Done!"
