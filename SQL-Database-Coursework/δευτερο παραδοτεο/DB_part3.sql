--1 
CREATE PROCEDURE CountCustomersInArea 
    @GeoCode INT
AS
BEGIN
    -- Counting the number of customers in the specified geographical area
    SELECT COUNT(*) AS NumberOfCustomers
    FROM Customer
    WHERE GeoCode = @GeoCode;
END;

--2 

CREATE PROCEDURE GetProductSupplies 
    @ProductCode INT, 
    @StartDate DATETIME, 
    @EndDate DATETIME
AS
BEGIN
    -- Declare variables
    DECLARE @SupplyCode INT, @Quantity INT, @SupplyDate DATETIME, @Description VARCHAR(300)

    -- Get the product description
    SELECT @Description = DESCRIPTION FROM Products WHERE Pcode = @ProductCode

    -- Print the product description
    PRINT 'Product Description: ' + @Description

    -- Declare the cursor
    DECLARE supplies_cursor CURSOR FOR 
        SELECT Purchases.Tcode, Purchases.Quantity, Purchases.Date 
        FROM Purchases 
        WHERE Purchases.Pcode = @ProductCode AND Purchases.Date BETWEEN @StartDate AND @EndDate

    -- Open the cursor
    OPEN supplies_cursor

    -- Fetch the first row from the cursor
    FETCH NEXT FROM supplies_cursor INTO @SupplyCode, @Quantity, @SupplyDate

    -- Loop through all rows
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Print supply details
        PRINT 'Supply Code: ' + CAST(@SupplyCode AS VARCHAR(10)) + ', Quantity: ' + CAST(@Quantity AS VARCHAR(10)) + ', Date: ' + CONVERT(VARCHAR, @SupplyDate, 120)

        -- Fetch next row from the cursor
        FETCH NEXT FROM supplies_cursor INTO @SupplyCode, @Quantity, @SupplyDate
    END

    -- Close and deallocate the cursor
    CLOSE supplies_cursor
    DEALLOCATE supplies_cursor
END


--3
import java.sql.*;
import java.util.Scanner;

public class CustomerDeletionApp {
    // Database URL, username and password
    static final String DB_URL = "jdbc:yourdburl"; // Replace with your database URL
    static final String USER = "username";         // Replace with your database username
    static final String PASS = "YOUR_DB_PASSWORD_HERE";         // Replace with your database password

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter client code to delete: ");
        int custCode = scanner.nextInt();

        deleteCustomer(custCode);
    }

    private static void deleteCustomer(int custCode) {
        Connection conn = null;
        Statement stmt = null;

        try {
            // Open a connection
            System.out.println("Connecting to database...");
            conn = DriverManager.getConnection(DB_URL, USER, PASS);

            // Execute a query to delete customer-related data
            System.out.println("Deleting customer data...");
            stmt = conn.createStatement();

            // Assuming CASCADE DELETE is not set, manually delete customer related data
            String sqlOrderDetails = "DELETE FROM OrderInclude WHERE CustCode = " + custCode;
            stmt.executeUpdate(sqlOrderDetails);

            String sqlOrders = "DELETE FROM Orders WHERE CustCode = " + custCode;
            stmt.executeUpdate(sqlOrders);

            String sqlPayments = "DELETE FROM Specialpayments WHERE CustCode = " + custCode;
            stmt.executeUpdate(sqlPayments);

            String sqlSpecialCustomers = "DELETE FROM Special_Customers WHERE CustCode = " + custCode;
            stmt.executeUpdate(sqlSpecialCustomers);

            String sqlCustomer = "DELETE FROM Customer WHERE CustCode = " + custCode;
            stmt.executeUpdate(sqlCustomer);

            System.out.println("Customer and related data deleted successfully.");
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } finally {
            // Finally block used to close resources
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException se2) {
            } // nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
    }
}

--4 

import java.sql.*;
import java.util.Scanner;

public class OrderDetailsApp {

    public static void main(String[] args) {
        String connectionString = "jdbc:sqlserver://[server-name];databaseName=[database-name];user=[username];password=[db-password]";
        
        try (Connection con = DriverManager.getConnection(connectionString);
             Scanner scanner = new Scanner(System.in)) {

            System.out.print("Enter Order Code: ");
            int orderCode = scanner.nextInt();
            
            printOrderDetails(con, orderCode);

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private static void printOrderDetails(Connection con, int orderCode) throws SQLException {
        String query = "SELECT O.ReferenceCode, O.OrderDate, O.Shipping, P.Name, I.Quantity, P.Price " +
                       "FROM Orders O " +
                       "JOIN OrderInclude I ON O.ReferenceCode = I.ReferenceCode " +
                       "JOIN Products P ON I.Pcode = P.Pcode " +
                       "WHERE O.ReferenceCode = ?";

        try (PreparedStatement stmt = con.prepareStatement(query)) {
            stmt.setInt(1, orderCode);
            ResultSet rs = stmt.executeQuery();

            boolean hasResults = false;
            while (rs.next()) {
                if (!hasResults) {
                    System.out.println("Order Details for Order Code: " + rs.getInt("ReferenceCode"));
                    System.out.println("Order Date: " + rs.getDate("OrderDate"));
                    System.out.println("Shipping Date: " + rs.getDate("Shipping"));
                    System.out.println("-----------------------------------");
                    hasResults = true;
                }
                System.out.println("Product: " + rs.getString("Name"));
                System.out.println("Quantity: " + rs.getInt("Quantity"));
                System.out.println("Price per unit: " + rs.getBigDecimal("Price"));
                System.out.println("-----------------------------------");
            }

            if (!hasResults) {
                System.out.println("No details found for Order Code: " + orderCode);
            }
        }
    }
}
