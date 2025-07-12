
/*

Business Context:

GL-Beats is a music-based startup that recently started selling music records online in multiple countries 
across the world. 
The executives at GL-Beats want to conduct a performance review and need recommendations on:

    Which music genres should their customers be recommended?
    Which artists need to be contracted within specific countries based on their popularity?

 
Objective:

As data scientists, our objective is to explore the available data by writing basic SQL queries 
and becoming familiar with the dataset. Additionally, we aim to answer the key business questions 
posed by top management, providing insights that can drive strategic decision-making.

*/



-- [1] How to retrieve all the rows of data present in our table album?

USE gl_beats;

SELECT *
FROM album;

/* Select * will fetch all the column details present in the table.*/

-- [2] How many rows of data are present in our table customers?

SELECT 
	COUNT(*) 
FROM customers;

/* Count * will count the number of rows present in the table.*/

-- [3] In order to show sample rows to the top management, write a query to show only 5 rows from the table artist.

SELECT *
FROM artist
LIMIT 5;

/* Limit 5 will fetch only 5 rows. It will restrict the rows to the number specified.*/

-- [4] Write a query to retrieve the unique playlist in our database.

SELECT 
	DISTINCT playlist_name
FROM playlist;


/* The distinct function will fetch the unique values of any columns.*/

-- [5]  Write a query to fetch the unique artists present in our database?

SELECT 
	DISTINCT artist_name
FROm artist;

-- [6] Write a query to count the customers in the country of Brazil?

SELECT
	 COUNT(DISTINCT customer_id) AS count_of_cust
FROM customers
WHERE customer_country = 'Brazil';

/* With the help of the where clause, we can define any condition.
A distinct count will count the unique values in the table.*/

-- [7] Write a query to count the number of artists?

SELECT 
	COUNT(DISTINCT artist_id) AS no_of_artist
FROM artist;

-- [8] Write a query to count the number of customers in the countries of Brazil, Germany, and Canada.

SELECT
	COUNT(DISTINCT customer_id) AS count_of_cust
FROM customers
WHERE customer_country IN ('Brazil','Germany','Canada');

/* If we want to compare more than one value in the where clause, we can use IN operator to do so.*/

-- [9] Write a query to retrieve information about customers with customer IDs ranging from 1 to 10.

SELECT *
FROM customers
WHERE customer_id BETWEEN 1 and 10;

/* We can compare a range of values in the where clause by using the between operator.*/

-- [10] Write a query to fetch the details of the tracks whose duration is between 100000 and 500000 and whose price is 0.99.

SELECT *
FROM tracks
WHERE (milliseconds BETWEEN 100000 AND 500000) AND (unit_price = 0.99); 

/* With the help of the AND operator, we can use two more than two conditions in the where clause.
With the help of AND operator, only those results will get displayed when all the conditions are satisfied. */

-- [11] Write a query to fetch the details of the tracks whose duration is in between 100000 and 500000 or whose price is 0.99?

SELECT *
FROM tracks
WHERE (milliseconds BETWEEN 100000 AND 500000) OR (unit_price = 0.99);

/* With the OR operator, the results will get displayed if any one of the given conditions is satisfied. */

-- [12] Write a query to get all the details for the customers whose first name starts with L?

SELECT *
FROM customers
 WHERE first_name LIKE 'L%';

/* We can compare the string values by using a LIKE operator.
L% means fetch those results where the first name's first letter should be L.*/

-- [13] Write a query to get all the details for the customers whose first name ends with K?

SELECT *
FROM customers
WHERE first_name LIKE '%K';

/* We can compare the string values by using the LIKE operator.
%L means fetch those results where the first name's last letter should be K.*/

-- [14] Write a query to fetch the details of the customer whose first name is Dan.

SELECT *
FROM customers
WHERE first_name = 'Dan';

/* We can compare the values with the help of the "=" operator in the where clause. */

-- [15] Write a query to fetch the details of the tracks whose unit price should not be equal to $0.90 and also the genre ID should not be equal to 18.

SELECT *
FROM tracks
WHERE unit_price <> 0.90 AND genre_id != 18;

/* The sign "<>" and "!=" denotes not equals to. */

-- [16] Write a query to fetch the details of the tracks where the unit price is greater than 0.90 $?

SELECT *
FROM tracks
WHERE unit_price > 0.90;

/* This query will fetch all the column values when the unit price is greater than 0.90. */

-- [17] Write a query to fetch the details of the tracks whose genre id is 10.

SELECT 	
	track_id
FROM tracks
WHERE genre_id =10;

/* This query will retrieve the track id and track name from the tracks table, as specified in the select statement, and whose genre id is 10.*/

-- [18] Write a query to fetch the details of the tracks for the genre id greater than 10?

SELECT 	
	track_id
FROM tracks
WHERE genre_id  > 10;

/* 
This query will retrieve the track id and track name from the tracks table, 
as specified in the select statement, and whose genre id is greater than 10.
*/

-- [19]  Write a query to fetch the invoices for the billing city of Edmonton, and also the billing price should be greater than 8 dollars.

SELECT *
FROM invoice
WHERE billing_city = 'Edmonton' AND total_price > 8;

/* 
This query will return all invoices from the billing city of Edmonton, 
and the total price must be greater than $8. 
*/

-- [20] Write a query to fetch the invoices whose billing city is Berlin or Paris and the invoice date is 2009-02-01.

SELECT *
FROM invoice
WHERE invoice_date = '2009-02-01' AND (billing_city = 'Berlin' OR billing_city = 'Paris');

/* This query will return all invoices from the billing cities of Berlin or Paris, with an invoice date of 2009-02-01. */


-- [21] Write a query to retrieve number of invoices in each city from invoice table in descending order.
SELECT billing_city, COUNT(invoice_id) as cnt_city
FROM invoice
GROUP BY billing_city
ORDER BY COUNT(billing_city) DESC;

/* This query will get the count of invoices  for each city from the invoice table & sort them in descending order of count */

-- [22] Write a query to get the revenue generated in each city from invoice table in descending order of cities.
SELECT billing_city, SUM(total_price) AS Total_Revenue
FROM invoice
GROUP BY billing_city
ORDER BY 2 DESC;

/* This query will get the revenue for each city from the invoice table & sort them in descending order of revenue */

-- [23] Write a query to get the number of customers for each country that have number of customers more than 5 from customers table.
SELECT customer_country, COUNT(customer_id) AS no_of_customers
FROM customers
GROUP BY 1
HAVING count(customer_id)>5
ORDER BY 2;

/* This query will get the list of countries that have more than 5 customers and sort them in descending order no of cusomters */
