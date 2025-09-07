-- MLS 1 - Questions to be answered

USE gl_beats;


-- 1. How to retrieve all the rows of data present in our table album?
<<<<<<< HEAD
 SELECT *
 FROM album;
 
-- 2. How many rows of data are present in our table customers?
SELECT COUNT(*)
FROM customers;



-- 3. In order to show sample rows to the top management, write a query to show only 5 rows from the table artist.

 SELECT *
 FROM artist
 LIMIT 5;


-- 4. Write a query to retrieve the unique playlist in our database.

 SELECT DISTINCT playlist_name
 FROM playlist;

-- 5. Write a query to fetch the unique artists present in our database?
 SELECT DISTINCT artist_name
 FROM artist;

-- 6. Write a query to count the customers in the country of Brazil?
SELECT
COUNT(customer_id)
FROM customers
WHERE customer_country = 'Brazil';

-- 7. Write a query to count the number of artists?

SELECT COUNT(artist_id)
FROM artist;

-- 8. Write a query to count the number of customers in the countries of Brazil, Germany, and Canada.

SELECT
COUNT(customer_id) AS customer_cnt
FROM customers
WHERE customer_country IN ( 'Brazil', 'Germany', 'Canada' );

-- 9. Write a query to retrieve information about customers with customer IDs ranging from 1 to 10.

SELECT *
FROM customers
WHERE customer_id BETWEEN 1 AND 10;


-- 10. Write a query to fetch the details of the tracks whose duration is between 100000 and 500000 and whose price is 0.99.

SELECT *
FROM tracks
WHERE ( milliseconds BETWEEN 100000 AND 500000 ) AND (unit_price = 0.99 )  ;



-- 12. Write a query to get all the details for the customers whose first name starts with L?

SELECT *
FROM customers
WHERE first_name LIKE 'L%';

-- 13. Write a query to get all the details for the customers whose first name ends with L?
SELECT *
FROM customers
WHERE first_name LIKE '%L';

=======

-- 2. How many rows of data are present in our table customers?

-- 3. In order to show sample rows to the top management, write a query to show only 5 rows from the table artist.

-- 4. Write a query to retrieve the unique playlist in our database.

-- 5. Write a query to fetch the unique artists present in our database?

-- 6. Write a query to count the customers in the country of Brazil?

-- 7. Write a query to count the number of artists?

-- 8. Write a query to count the number of customers in the countries of Brazil, Germany, and Canada.

-- 9. Write a query to retrieve information about customers with customer IDs ranging from 1 to 10.

-- 10. Write a query to fetch the details of the tracks whose duration is between 100000 and 500000 and whose price is 0.99.

-- 11. Write a query to fetch the details of the tracks whose duration is in between 100000 and 500000 or whose price is 0.99?

-- 12. Write a query to get all the details for the customers whose first name starts with L?

-- 13. Write a query to get all the details for the customers whose first name ends with L?
>>>>>>> dde1ce1463f16c97974bd1ec2506f6088cddb0e5

-- 14. Write a query to fetch the details of the customer whose first name is Dan.

-- 15. Write a query to fetch the details of the tracks whose unit price should not be equal to $0.90 and also the genre ID should not be equal to 18.

-- 16. Write a query to fetch the details of the tracks where the unit price is greater than 0.90 $?

-- 17. Write a query to fetch the details of the tracks whose genre id is 10.

-- 18. Write a query to fetch the details of the tracks for the genre id greater than 10?

-- 19. Write a query to fetch the invoices for the billing city of Edmonton, and also the billing price should be greater than 8 dollars.

-- 20. Write a query to fetch the invoices whose billing city is Berlin or Paris and the invoice date is 2009-02-01.

-- 21. Write a query to retrieve number of invoices in each city from invoice table in descending order.

-- 22. Write a query to get the revenue generated in each city from invoice table in descending order of cities.

-- 23. Write a query to get the number of customers for each country that have number of customers more than 5 from customers table.
<<<<<<< HEAD
=======

>>>>>>> dde1ce1463f16c97974bd1ec2506f6088cddb0e5
