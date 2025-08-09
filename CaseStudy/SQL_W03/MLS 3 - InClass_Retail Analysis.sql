/*--------------------------------------------
    SECTION-01: Data Exploration
--------------------------------------------*/
USE retail_analysis;

/* Question 1:
List all customers who have not placed any orders. */
SELECT FirstName, LastName
FROM customer
WHERE Id NOT IN (SELECT CustomerId FROM orders);
-- This query shows customers who haven't placed any orders.

/* Question 2:
Retrieve the names of products that have never been ordered. */
SELECT ProductName
FROM product
WHERE Id NOT IN (SELECT ProductId FROM orderitem);
-- This query returns products that have never been bought.

/* Question 3:
Identify the top 3 customers who have spent the most on orders. */
SELECT FirstName, LastName, TotalSpent
FROM (
  SELECT c.FirstName, 
         c.LastName, 
         ROUND(SUM(o.TotalAmount),2) AS TotalSpent
  FROM customer c
  LEFT JOIN orders o ON c.Id = o.CustomerId
  GROUP BY 
		c.FirstName, 
        c.LastName
) AS CustomerSpending
ORDER BY TotalSpent DESC
LIMIT 3;
-- This query displays the top 3 customers on number of orders.

/* Question 4:
For each supplier, show the total number of unique products sold at least once */
SELECT s.CompanyName, COUNT(DISTINCT p.Id) AS TotalProductsSupplied
FROM supplier s
JOIN product p ON s.Id = p.SupplierId
WHERE p.Id IN (
  SELECT DISTINCT ProductId
  FROM orderitem
)
GROUP BY s.CompanyName;
-- This query shows the total number of unique products offered by the suppliers.

/* Question 5:
Identify the average spending per order for each customer who has placed more than one order. */
SELECT c.FirstName, 
       c.LastName, 
       ROUND((CustomerOrderTotals.TotalSpent / CustomerOrderTotals.OrderCount),2) AS AvgSpendingPerOrder
FROM customer c
JOIN (
  SELECT CustomerId, 
         SUM(TotalAmount) AS TotalSpent, 
         COUNT(Id) AS OrderCount
  FROM orders
  GROUP BY CustomerId
) AS CustomerOrderTotals ON c.Id = CustomerOrderTotals.CustomerId
WHERE CustomerOrderTotals.OrderCount > 1;
-- This query displays the customer names and their average order amount for customers who have ordered more than once.

/* Question 6:
Identify the most popular product for each customer based on quantity ordered. */
SELECT CustomerId, FirstName, LastName, ProductName
FROM (
    SELECT c.Id AS CustomerId, c.FirstName, c.LastName, p.ProductName,
           SUM(oi.Quantity) AS TotalQuantity,
           RANK() OVER (PARTITION BY c.Id ORDER BY SUM(oi.Quantity) DESC) AS rnk
    FROM customer c
    JOIN orders o ON c.Id = o.CustomerId
    JOIN orderitem oi ON o.Id = oi.OrderId
    JOIN product p ON oi.ProductId = p.Id
    GROUP BY c.Id, p.Id, c.FirstName, c.LastName, p.ProductName
) AS RankedProducts
WHERE rnk = 1;
-- This query identifies the most populat product for each customer based on quantity.

/* Question 7:
Display the average order amount for customers whose average order amount is higher than the overall average. */
SELECT coa.CustomerId, coa.FirstName, coa.LastName, coa.AvgOrderAmount
FROM (
    SELECT c.Id AS CustomerId, c.FirstName, c.LastName,
            ROUND(AVG(o.TotalAmount),2) AS AvgOrderAmount
    FROM customer c
    JOIN orders o ON c.Id = o.CustomerId
    GROUP BY c.Id, c.FirstName, c.LastName
) AS coa
WHERE coa.AvgOrderAmount > (
    SELECT AVG(TotalAmount)
    FROM orders
);
-- This query identifies average order amounts for the customers whose average is higher than average.


/* -----------------------------------
    SECTION-02: Recommendations
------------------------------------*/

-- The top 5 products that contribute the most to revenue (calculated as unit price * quantity sold) across all orders.
SELECT ProductName, Revenue
FROM (
  SELECT p.ProductName, 
         ROUND(SUM(oi.UnitPrice * oi.Quantity),2) AS Revenue
  FROM product p
  JOIN orderitem oi ON p.Id = oi.ProductId
  GROUP BY p.ProductName
) AS ProductRevenue
ORDER BY Revenue DESC
LIMIT 5;
-- These are the top 5 products that contribute the most to revenue.

-- Supplier's name and the name of their best-selling product (in terms of quantity) that has been ordered.
SELECT CompanyName, ProductName, TotalQuantitySold
FROM (
  SELECT s.CompanyName, 
         p.ProductName, 
         SUM(oi.Quantity) AS TotalQuantitySold,
         RANK() OVER (PARTITION BY s.CompanyName ORDER BY SUM(oi.Quantity) DESC) AS rnk
  FROM supplier s
  LEFT JOIN product p ON s.Id = p.SupplierId
  LEFT JOIN orderitem oi ON p.Id = oi.ProductId
  GROUP BY s.Id, s.CompanyName, p.Id, p.ProductName
) AS BestSellingProducts
WHERE rnk = 1;
-- These are the best-selling products for each supplier.