
--1
--Δείξε μία λίστα των πελατών με τον κωδικό τους, το ΑΦΜ τους, την επωνυμία τους, τη διευθυνσή τους και το τηλεφωνό τους. *
-- Replace with the target database name before running.
use YOUR_DB_NAME_HERE
select CustCode, CusVat, CusName, Street, Number, City, PostalCode, CusPhone
FROM Customers;

--2
--Για κάθε κωδικό πελάτη δείξε τις πληρωμές που έχει κάνει στο διάστημα 12/5/2022 εώς 22/5/2022. *
SELECT CustCode, Amount
FROM Specialpayments
WHERE Date BETWEEN '2022-05-12' AND '2022-05-22'
Group By CustCode, Amount;

--3
--Για κάθε παραγγελία δείξε την ημερομηνία της, τον κωδικό της και τους κωδικούς των προϊόντων που αγοράστηκαν. *

SELECT Orders.ReferenceCode, OrderDate, Products.Pcode
FROM Orders, Products, OrderInclude
where OrderInclude.ReferenceCode=Orders.ReferenceCode and OrderInclude.Pcode=Products.Pcode
group by Orders.ReferenceCode, OrderDate, Products.Pcode;

--4
--Αύξησε την τιμή όλων των προϊόντων κατά 3%. *

UPDATE Products
SET Price=Price + Price*3/100;

--5
--Δείξε για κάθε μήνα του 2022 το σύνολο και το μέσο όρο των πληρωμών.

SELECT MONTH(Date) as month, SUM(Amount) as sum, AVG(Amount) as avg
FROM Specialpayments
WHERE YEAR(Date)= 2022
GROUP BY MONTH(Date);

--6
--Δείξε το ΑΦΜ και την επωνυμία όλων των πελατών που έχουν κάνει συνολικές αγορές τον Ιανουάριο του 2023 πάνω από 2500€.
SELECT CusVat, CusName --, sum(Amount) as sum πληροφορια που δεν ζηταει η εκφωνηση να προβληθει 
FROM Customers, Specialpayments
WHERE Customers.CustCode=Specialpayments.CustCode 
Group by CusVat,CusName, Date
Having(MONTH(Date)=1 AND YEAR(Date)=2023 AND sum(Amount)>2500);

--7
-- Για κάθε πελάτη, δείξε ανά κατηγορία προϊόντων το σύνολο της αξίας των προϊόντων που έχει αγοράσει.

SELECT Cu.CustCode, Ca.CategoryCode, SUM(P.Price*OrderInclude.Quantity) as sum
FROM Customers as Cu, Category as Ca, Products as P, OrderInclude, Orders
WHERE Ca.CategoryCode=P.CategoryCode AND OrderInclude.Pcode=P.Pcode AND Cu.CustCode=Orders.CustCode AND Orders.ReferenceCode=OrderInclude.ReferenceCode
GROUP BY Ca.CategoryCode,Cu.CustCode ;

--8
--Δείξε το μέσο όρο των πωλήσεων ανά γεωγραφική περιοχή και κατηγορία.
SELECT Region.GeoCode, Category.CategoryCode, AVG(Price*Quantity) as Avg
FROM Region, Category, Products, OrderInclude, Orders, Customers
WHERE Region.GeoCode=Customers.GeoCode AND Category.CategoryCode=Products.CategoryCode and Products.Pcode=OrderInclude.Pcode AND Orders.CustCode=Customers.CustCode AND Orders.ReferenceCode=OrderInclude.ReferenceCode
GROUP BY Region.GeoCode, Category.CategoryCode;
GO


--9
--Για κάθε μήνα του 2022, δείξε τις συνολικές πωλήσεις του μήνα σαν ποσοστό των συνολικών ετήσιων πωλήσεων του 2022.
CREATE view V1 AS
SELECT MONTH(OrderDate) AS Month, SUM(Products.Price*OrderInclude.Quantity) AS TotalMonth
FROM OrderInclude, Products, Orders
WHERE YEAR(OrderDate)= 2022 AND OrderInclude.Pcode=Products.Pcode AND OrderInclude.ReferenceCode=Orders.ReferenceCode
GROUP BY MONTH(OrderDate);

GO
CREATE view V2 AS
SELECT SUM(Products.Price*OrderInclude.Quantity) AS TotalYear
FROM OrderInclude, Products, Orders
WHERE YEAR(OrderDate)= 2022 AND OrderInclude.Pcode=Products.Pcode AND OrderInclude.ReferenceCode=Orders.ReferenceCode;

GO

SELECT V1.Month, V1.TotalMonth/V2.TotalYear*100 AS Percentage
FROM V1, V2;

DROP VIEW V2, V1;

--10 Για κάθε μήνα, μέτρησε πόσοι πελάτες έχουν μέσο όρο αξίας αγορών μεγαλύτερο από το μέσο όρο του μήνα.

GO
CREATE view V1 AS
SELECT MONTH(OrderDate)AS Month, YEAR(OrderDate) as Year, Avg(Products.Price*OrderInclude.Quantity) AS AvgMonth
FROM OrderInclude, Products, Orders
WHERE OrderInclude.Pcode=Products.Pcode AND OrderInclude.ReferenceCode=Orders.ReferenceCode
GROUP BY MONTH(OrderDate),YEAR(OrderDate) ;

GO

create view V2 as
SELECT MONTH(OrderDate) AS Month,YEAR(OrderDate) as Year, Avg(Products.Price*OrderInclude.Quantity) AS AvgCus, Customers.CustCode 
FROM OrderInclude, Products, Orders, Customers
WHERE OrderInclude.Pcode=Products.Pcode AND OrderInclude.ReferenceCode=Orders.ReferenceCode and Customers.CustCode=Orders.CustCode
GROUP BY Customers.CustCode, MONTH(OrderDate), YEAR(OrderDate);

GO


select V1.Month,V1.Year, COUNT( DISTINCT V2.CustCode) AS CustomerCount
FROM V1, V2, Customers, Orders
WHERE V1.Month=V2.Month AND V1.Year=V2.Year and V2.AvgCus>V1.AvgMonth 
GROUP BY V1.Month, V1.Year;

DROP VIEW V2, V1;

--11 Για κάθε μήνα του 2022, σύγκρινε τις συνολικές πωλήσεις του μήνα σε σχέση με τον αντίστοιχο μήνα του 2021 (σαν ποσοστό).
GO
CREATE view V3 AS
SELECT MONTH(OrderDate) AS Month, SUM(Products.Price*OrderInclude.Quantity) AS TotalMonth
FROM OrderInclude, Products, Orders
WHERE YEAR(OrderDate)= 2022 AND OrderInclude.Pcode=Products.Pcode AND OrderInclude.ReferenceCode=Orders.ReferenceCode
GROUP BY MONTH(OrderDate);

GO
CREATE view V4 AS
SELECT MONTH(OrderDate) AS Month, SUM(Products.Price*OrderInclude.Quantity) AS TotalMonth
FROM OrderInclude, Products, Orders
WHERE YEAR(OrderDate)= 2021 AND OrderInclude.Pcode=Products.Pcode AND OrderInclude.ReferenceCode=Orders.ReferenceCode
GROUP BY MONTH(OrderDate);

GO

SELECT V3.Month, ((V3.TotalMonth-V4.TotalMonth)/V4.TotalMonth)*100 AS Percentage
FROM V3, V4
WHERE V3.Month=V4.Month;

Drop view V3, V4;

--12
--Δείξε για κάθε μήνα του 2022, το μέσο όρο πωλήσεων αυτού του μήνα και το μέσο όρο πωλήσεων κατά τους μήνες που προηγήθηκαν αυτού.

GO
CREATE view V5 AS
SELECT MONTH(OrderDate) AS Month, AVG(Products.Price*OrderInclude.Quantity) AS AvgMonth
FROM OrderInclude, Products, Orders
WHERE YEAR(OrderDate)= 2022 AND OrderInclude.Pcode=Products.Pcode AND OrderInclude.ReferenceCode=Orders.ReferenceCode
GROUP BY MONTH(OrderDate);

GO

CREATE VIEW V6 AS
SELECT V5.AvgMonth as Avg, V5.Month as Month
FROM V5
GROUP BY V5.Month, V5.AvgMonth

GO

SELECT V5.Month, V5.AvgMonth, (SELECT AVG(V6.Avg)
                                FROM V6
                                WHERE V6.Month < V5.Month) AS AvgMonthBefore
FROM V5, V6
WHERE V5.Month=V6.Month;

drop view V5, V6;

--13
--Δείξε τους κωδικούς των προϊόντων που όλοι οι προμηθευτές τους προέρχονται από την ίδια γεωγραφική περιοχή.


SELECT Products.Pcode
FROM Products, Purchases, Suppliers
WHERE Products.Pcode=Purchases.Pcode and Suppliers.Scode=Purchases.Scode
group by Products.Pcode
Having count(distinct Suppliers.GeoCode)=1;

--14
--Δείξε τον κωδικό των παραγγελιών όπου τα προϊόντα που περιέχουν προμηθεύονται από τουλάχιστον πέντε προμηθευτές.

WITH ProductSupplierCounts AS (
    SELECT
        Pcode,
        COUNT(DISTINCT Scode) AS SupplierCount
    FROM Purchases
    GROUP BY Pcode
)
SELECT
    O.ReferenceCode
FROM
    Orders O
    JOIN OrderInclude OI ON O.ReferenceCode = OI.ReferenceCode
    JOIN ProductSupplierCounts PSC ON OI.Pcode = PSC.Pcode
GROUP BY
    O.ReferenceCode
HAVING
    MIN(PSC.SupplierCount) >= 5;



SELECT DISTINCT(OrderInclude.Pcode), Orders.ReferenceCode, Purchases.Scode
FROM OrderInclude, Purchases, Orders
WHERE OrderInclude.Pcode=Purchases.Pcode AND Orders.ReferenceCode=OrderInclude.ReferenceCode
GROUP BY OrderInclude.Pcode, Orders.ReferenceCode, Purchases.Scode
HAVING COUNT(DISTINCT Purchases.Scode)<5;

go
SELECT DISTINCT(Orders.ReferenceCode)
FROM Orders, OrderInclude, Purchases
WHERE Orders.ReferenceCode=OrderInclude.ReferenceCode AND OrderInclude.Pcode=Purchases.Pcode
GROUP by OrderInclude.Pcode, Orders.ReferenceCode
HAVING COUNT(DISTINCT Purchases.Scode)>=5
EXCEPT (Select distinct(V7.ReferenceCode)
                        from V7
                        group by V7.Pcode, V7.ReferenceCode
                        HAVING COUNT(DISTINCT V7.Scode)<5);



WITH ProductSupplierCounts AS (
    SELECT
        Pcode,
        COUNT(DISTINCT Scode) AS SupplierCount
    FROM Purchases
    GROUP BY Pcode
)
SELECT
    O.ReferenceCode
FROM
    Orders O
    JOIN OrderInclude OI ON O.ReferenceCode = OI.ReferenceCode
    JOIN ProductSupplierCounts PSC ON OI.Pcode = PSC.Pcode
GROUP BY
    O.ReferenceCode
HAVING
    SUM(distinct PSC.SupplierCount) >= 5;
