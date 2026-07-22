/*
(1) Γράψτε μια stored procedure η οποία θα δέχεται τον κωδικό μίας γεωγραφικής περιοχής και θα
τυπώνει τον αριθμό των πελατών σε αυτή την περιοχή.
*/

CREATE PROCEDURE ex1
    @GeoCode INT
AS
BEGIN
    SELECT COUNT(*) AS NumberOfCustomers
    FROM Customers
    WHERE GeoCode = @GeoCode;
END;

--EXECUTE ex1 10001;

--DROP PROCEDURE ex1;
-------------------------------------------------------------------------------------------------------
/*
(2) Γράψτε μια stored procedure η οποία θα δέχεται τον κωδικό προϊόντος και δύο ημερομηνίες και
θα τυπώνει την περιγραφή του προϊόντος και όλες τις προμήθειες αυτού του προϊόντος στο
διάστημα μεταξύ των δύο ημερομηνιών (κωδικός προμήθειας, ποσότητα, ημερομηνία).
Χρησιμοποιείστε λογικούς δρομείς.
*/

GO

create PROCEDURE ex2
    @Pccode INT,
    @Start DATETIME,
    @End DATETIME
AS
BEGIN
    declare @description VARCHAR(300), @Tcode INT, @Quantity INT, @Date DATETIME;
    DECLARE Info CURSOR
        FOR SELECT DESCRIPTION, Tcode, Quantity, Date
        FROM Products, Purchases
        where Purchases.Pcode=Products.Pcode and Products.Pcode = @Pccode AND Purchases.Date BETWEEN @Start AND @End
        ORDER BY Date;
    OPEN Info;
    FETCH NEXT FROM Info INTO @description, @Tcode, @Quantity, @Date;
    PRINT 'Product Description: ' + @description
    WHILE @@FETCH_STATUS = 0
    BEGIN
        PRINT 'Transaction code ' + CAST(@Tcode AS VARCHAR(20)) + ', Quantity: ' + CAST(@Quantity AS VARCHAR(10)) + ', Date: ' + CONVERT(VARCHAR, @Date, 120);
        FETCH NEXT FROM Info INTO @description, @Tcode, @Quantity, @Date;
    END;

    CLOSE Info;
    DEALLOCATE Info;
END;

--EXECUTE ex2 30001, '2021-01-30', '2022-06-15';

--DROP PROCEDURE ex2;
