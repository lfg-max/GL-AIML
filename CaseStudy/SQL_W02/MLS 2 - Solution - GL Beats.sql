/*--------------------------------------------
    SECTION-01: Data Exploration
--------------------------------------------*/
USE gl_beats;
/* Question 1:
List the total sales for each year. */
SELECT 
    YEAR(invoice_date) AS YR, 
    SUM(total_price)
FROM 
    invoice
GROUP BY 
    YEAR(invoice_date);
-- In MySQL, you can simply use the YEAR() function to extract the year from a datatime data type. Eg: YEAR(invoice_date) AS YR.
-- Refer to the "Note - Inbuilt Functions" content page available on the dashboard for the differences in syntax between SQLite and MySQL.

/* Question 2:
Check the distribution of the month wise sales for the year 2010. */
SELECT 
    MONTH(invoice_date) AS MTH, 
    SUM(total_price)
FROM 
    invoice
WHERE
    YEAR(invoice_date) = 2010
GROUP BY 
    MONTH(invoice_date);
-- In MYSQL, you can simply use the YEAR() and MONTH() to extract the year and month from a datetime data type. Eg: MONTH(invoice_date) as MTH.
-- Refer to the "Note - Inbuilt Functions" content page available on the dashboard for the differences in syntax between SQLite and MySQL.

/* Question 3:
List the full names of the customers in decreasing order of sales. */    
    
SELECT 
    CONCAT(first_name, ' ', last_name) AS full_name, 
    SUM(total_price)
FROM 
    customers
    LEFT JOIN invoice USING(customer_id)
GROUP BY 
    full_name
ORDER BY 
    SUM(total_price) DESC;
    
    
-- In MySQL, you can use the CONCAT() function to combine two strings. Eg: CONCAT(first_name, last_name) AS full_name.
-- Refer to the "Note - Inbuilt Functions" content page available on the dashboard for the differences in syntax between SQLite and MySQL.

/* Question 4:
List all artists with their respective albums names, including artists with no albums. */
SELECT 
    artist.artist_name AS Artist,
    album.title_name AS Album
FROM 
    artist
    LEFT JOIN album ON album.artist_id = artist.artist_id;
-- This query displays all artists present in the database irrespective of whether they have any linked albums.

/* Question 5:
Display each artist along with the count of albums they have produced, including artists with no albums. */
SELECT 
    artist.artist_name AS Artist, 
    COUNT(album.album_id) AS Album_Count
FROM 
    artist
    LEFT JOIN album ON artist.artist_id = album.artist_id
GROUP BY 
    artist.artist_name;
-- This query will return all artists along with the count of all albums they have produced.

/* Question 6:
Identify the total revenue for each album by summing the total prices from all invoices associated with the album. */
SELECT
    al.title_name AS album_title,
    SUM(ii.unit_price * ii.quantity) AS total_revenue
FROM
    invoice_items ii
    INNER JOIN tracks t ON ii.track_id = t.track_id
    INNER JOIN album al ON t.album_id = al.album_id
    INNER JOIN artist ar ON al.artist_id = ar.artist_id
GROUP BY
    al.title_name; 
-- This query displays the total revenue for each album along with the artist's name.


/* -----------------------------------
    SECTION-02: Recommendations
------------------------------------*/

/* Question 1:
What are the most popular genres in each country, ranked by the number of purchases? */
SELECT 
    c.customer_country, 
    g.genre_name, 
    COUNT(ii.invoice_line_id) AS purchase_count
FROM 
    invoice_items ii
    JOIN invoice i ON ii.invoice_id = i.invoice_id
    JOIN customers c ON i.customer_id = c.customer_id
    JOIN tracks t ON ii.track_id = t.track_id
    JOIN genre g ON t.genre_id = g.genre_id
GROUP BY 
    c.customer_country, 
    g.genre_name
ORDER BY 
    purchase_count DESC, 
    c.customer_country;
-- This query provides insight on the most popular genres in each country.

/* Question 2:
Which artists are the most popular in each country? */
SELECT 
    c.customer_country, 
    ar.artist_name, 
    COUNT(ii.invoice_line_id) AS purchase_count
FROM 
    invoice_items ii
    JOIN invoice i ON ii.invoice_id = i.invoice_id
    JOIN customers c ON i.customer_id = c.customer_id
    JOIN tracks t ON ii.track_id = t.track_id
    JOIN album al ON t.album_id = al.album_id
    JOIN artist ar ON al.artist_id = ar.artist_id
GROUP BY 
    c.customer_country, 
    ar.artist_name
ORDER BY 
    purchase_count DESC, 
    c.customer_country;
-- Using this query, you can find out the most popular artists in each country.




-- Additional for later

WITH ArtistPurchases AS (
    -- This first part is your original query to get the counts for each artist in each country
    SELECT 
        c.customer_country, 
        ar.artist_name, 
        COUNT(ii.invoice_line_id) AS purchase_count
    FROM 
        invoice_items ii
        JOIN invoice i ON ii.invoice_id = i.invoice_id
        JOIN customers c ON i.customer_id = c.customer_id
        JOIN tracks t ON ii.track_id = t.track_id
        JOIN album al ON t.album_id = al.album_id
        JOIN artist ar ON al.artist_id = ar.artist_id
    GROUP BY 
        c.customer_country, 
        ar.artist_name
),
RankedArtists AS (
    -- Now, we rank each artist within their country based on the purchase count
    SELECT
        customer_country,
        artist_name,
        purchase_count,
        RANK() OVER(PARTITION BY customer_country ORDER BY purchase_count DESC) AS artist_rank
    FROM
        ArtistPurchases
)
-- Finally, select only the artists with the top rank (rank = 1) for each country
SELECT
    customer_country,
    artist_name,
    purchase_count
FROM
    RankedArtists
WHERE
    artist_rank = 1
ORDER BY
    customer_country;