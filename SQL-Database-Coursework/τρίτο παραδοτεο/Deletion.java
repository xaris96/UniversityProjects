import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;

public class Deletion {
    private static final String dbName = System.getenv("DB_NAME") != null && !System.getenv("DB_NAME").isBlank()
            ? System.getenv("DB_NAME")
            : "YOUR_DB_NAME_HERE";
    private static final String dbUser = System.getenv("DB_USER") != null && !System.getenv("DB_USER").isBlank()
            ? System.getenv("DB_USER")
            : "YOUR_DB_USER_HERE";
    private static final String dbPassword= System.getenv("DB_PASSWORD") != null && !System.getenv("DB_PASSWORD").isBlank()
            ? System.getenv("DB_PASSWORD")
            : "YOUR_DB_PASSWORD_HERE";
    public static void main(String[] args) {
        Connection dbcon = null;
        Statement stmt = null ;
        ResultSet rs = null;
        String url = "jdbc:sqlserver://sqlserver.dmst.aueb.gr:1433;"
        + "databaseName=" + dbName + ";user=" + dbUser + ";password=" + dbPassword + ";encrypt=true;trustServerCertificate=true;";
        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        } catch(java.lang.ClassNotFoundException e) {
            System.out.println("ClassNotFoundException: " + e.getMessage());
            System.exit(0);
        }
		try {
			dbcon = DriverManager.getConnection(url);
        } catch (SQLException e) {
			System.out.println("SQLException: " + e.getMessage());
			System.exit(0);
		}
        try{
            Scanner sc = new Scanner(System.in);
            System.out.println("Enter customer id: ");
            int id = sc.nextInt();
            stmt = dbcon.createStatement();
            String checkSql = "SELECT CustCode FROM Customers WHERE CustCode = " + id;
            rs = stmt.executeQuery(checkSql);
            if (rs.next()) {
                // Check if customer exists in Special_Customers table
                checkSql = "SELECT * FROM Special_Customers WHERE CustCode = " + id; //not all customers are special
                rs = stmt.executeQuery(checkSql);
                String deleteSql;
                if (rs.next()) {
                    
                    checkSql = "SELECT * FROM Orders WHERE CustCode = " + id; //not all customers have orders
                    rs = stmt.executeQuery(checkSql);
                    if (rs.next()) {
                        deleteSql = "DELETE FROM OrderInclude WHERE OrderInclude.ReferenceCode IN (SELECT Orders.ReferenceCode FROM Orders WHERE Orders.CustCode=" + id + ")";
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM Orders WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM SpecialPayments WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM Special_Customers WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM Customers WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        System.out.println("Customer deleted successfully");
                    } else {
                        deleteSql = "DELETE FROM SpecialPayments WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM Special_Customers WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM Customers WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        System.out.println("Customer deleted successfully");
                    }
                } else {
                    checkSql = "SELECT * FROM Orders WHERE CustCode = " + id; //not all customers have orders
                    rs = stmt.executeQuery(checkSql);
                    if (rs.next()) {
                        deleteSql = "DELETE FROM OrderInclude WHERE OrderInclude.ReferenceCode IN (SELECT Orders.ReferenceCode FROM Orders WHERE Orders.CustCode=" + id + ")";
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM Orders WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        deleteSql = "DELETE FROM Customers WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        System.out.println("Customer deleted successfully");
                        
                    } else {
                        deleteSql = "DELETE FROM Customers WHERE CustCode = " + id;
                        stmt.executeUpdate(deleteSql);
                        System.out.println("Customer deleted successfully");
                    }
                }
            } else {
                System.out.println("Invalid Customer ID");
            }
            sc.close();
            rs.close();
            stmt.close();
            dbcon.close();
        }
        catch(SQLException e) {
            System.out.println("SQLException: " + e.getMessage());
        } finally {
            try {
                dbcon.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
