#/bin/bash

execute_query () {
	mysql -h $db_host -u $db_user -p$db_pass -D klaudijus -e "$1"	 
}
#DROP TABLES
echo "Deleting tables ..."
execute_query 'DROP TABLE person'
execute_query 'DROP TABLE drink'

#Recreate tables
echo "Creating tables..."
execute_query 'CREATE TABLE person (person_id INTEGER AUTO_INCREMENT PRIMARY KEY,display_name VARCHAR(100),name VARCHAR(100),team VARCHAR(100), favDrink_id INTEGER, PMUDrink_id Integer)'

execute_query 'CREATE TABLE drink (drink_id INTEGER AUTO_INCREMENT PRIMARY KEY,display_name VARCHAR(100),drink_type VARCHAR(100),recipe VARCHAR(100))'

#Insert people
execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("David", "david","Academy" , 1, 2)'
execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("Henry", "henry","Academy" , 2, 3)'
execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("Charlie", "charlie","Academy" , 1, 2)'
execute_query 'INSERT INTO `person`(display_name, name, team, FavDrink_id, PMUDrink_id) VALUES ("Lindsay", "lindsay","Hermes" , 3, 4)'


echo "Done!"
