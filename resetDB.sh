#/bin/bash

execute_query () {
	mysql -h $DB_HOST -u $DB_USER -p$DB_PASS -D klaudijus -e "$1"	 
}
#DROP TABLES
echo "Deleting tables ..."
execute_query 'DROP TABLE person'
execute_query 'DROP TABLE drink'

#Recreate tables
echo "Creating tables..."

execute_query 'CREATE TABLE drink (drink_id INTEGER AUTO_INCREMENT PRIMARY KEY,display_name VARCHAR(100),drink_type VARCHAR(100),recipe VARCHAR(100))'

execute_query 'CREATE TABLE person (person_id INTEGER AUTO_INCREMENT PRIMARY KEY, display_name VARCHAR(100), name VARCHAR(100), team VARCHAR(100), favDrink_id INTEGER , PMUDrink_id INTEGER, FOREIGN KEY(favDrink_id) REFERENCES drink(drink_id) ON DELETE CASCADE , FOREIGN KEY(PMUDrink_id) REFERENCES drink(drink_id) ON DELETE CASCADE)'

#Insert Drinks
echo "Inserting Drinks"

execute_query 'INSERT INTO `drink`(display_name, drink_type, recipe) VALUES ("Coffee","coffee",NULL)'

execute_query 'INSERT INTO `drink`(display_name, drink_type, recipe) VALUES ("Water","cold",NULL)'

execute_query 'INSERT INTO `drink`(display_name, drink_type, recipe) VALUES ("Tea","hot",NULL)'

#Insert people
echo "Inserting People"

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("Charlie", "charlie","Academy" , 1, 2)'

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("Henry", "henry","Academy" , 2, 3)'

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("David", "david","Academy" , 3, 1)'

execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("Lindsay", "lindsay","Hermes" , 1, 3)'


echo "Done!"
