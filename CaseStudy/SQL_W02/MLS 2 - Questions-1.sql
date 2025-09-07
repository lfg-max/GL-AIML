-- MLS 2 - Questions to be answered

-- Section 1:

-- 1. List the total sales for each year.

SELECT
YEAR(invoice_date) as Year,
SUM(total_price)
FROM invoice
GROUP BY Year;


-- 2. Check the distribution of the month wise sales for the year 2010.

SELECT
MONTH(invoice_date) as MNTH,
SUM(total_price)
FROM invoice
WHERE YEAR(invoice_date) = 2010
GROUP BY MNTH;



-- 3. List the full names of the customers in decreasing order of sales.


SELECT
CONCAT(first_name, ' ', last_name) AS cust_name,
SUM(total_price) as sales

FROM
customers
LEFT JOIN invoice USING(customer_id)

GROUP BY cust_name

ORDER BY sales DESC;



-- 4. List all artists with their respective albums names, including artists with no albums.

SELECT
artist_name,
title_name

FROM
artist ar
LEFT JOIN album al ON ar.artist_id = al.artist_id;






-- 5. Display each artist along with the count of albums they have produced, including artists with no albums.

SELECT
artist_name,
COUNT(album_id) as album_count

FROM
artist ar
LEFT JOIN album al ON ar.artist_id = al.artist_id

GROUP BY artist_name;




-- 6. Identify the total revenue for each album by summing the total prices from all invoices associated with the album.

SELECT
al.title_name as Album_title,
SUM(ii.unit_price * ii.quantity ) as revenue

FROM
invoice_items ii
INNER JOIN tracks t ON ii.track_id = t.track_id
INNER JOIN album al ON t.album_id = al.album_id

GROUP BY al.title_name;







-- Section 2:

-- 1. What are the most popular genres in each country, ranked by the number of purchases?

SELECT
c.customer_country as country,
g.genre_name as genre,
COUNT(ii.invoice_line_id) as purchase_count

FROM
customers c
INNER JOIN invoice i ON i.customer_id = c.customer_id
INNER JOIN invoice_items ii ON ii.invoice_id = i.invoice_id
INNER JOIN tracks t ON ii.track_id = t.track_id
INNER JOIN genre g ON t.genre_id = g.genre_id

GROUP BY
country,
genre

ORDER BY
purchase_count DESC;


-- 2. Which artists are the most popular in each country?

SELECT
c.customer_country as country,
ar.artist_name as artist_name,
COUNT(ii.invoice_line_id) as purchase_count

FROM
customers c
INNER JOIN invoice i ON i.customer_id = c.customer_id
INNER JOIN invoice_items ii ON ii.invoice_id = i.invoice_id
INNER JOIN tracks t ON ii.track_id = t.track_id
INNER JOIN album a ON t.album_id = a.album_id
INNER JOIN artist ar ON a.artist_id = ar.artist_id


GROUP BY
country,
genre

ORDER BY
purchase_count DESC;



