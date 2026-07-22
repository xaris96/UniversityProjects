import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;

public class OrderDetails {
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
        Statement stmt2 = null ;
        Statement stmt3 = null ;
        ResultSet rs = null;
        ResultSet rb = null;
        ResultSet ra = null;
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
            System.out.println("Enter order id: ");
            int id = sc.nextInt();
            stmt = dbcon.createStatement();
            stmt2 = dbcon.createStatement();
            stmt3 = dbcon.createStatement();
            String sql1 = "SELECT * FROM Orders WHERE ReferenceCode = " + id;
            rs=stmt.executeQuery(sql1);
            String sql2 = "SELECT * FROM OrderInclude, Products WHERE OrderInclude.Pcode=Products.Pcode and ReferenceCode = " + id;
            rb=stmt2.executeQuery(sql2);
            String sql3= "Select Title, Category.Description from Category, OrderInclude, Products where Products.Pcode= OrderInclude.Pcode and Products.CategoryCode= Category.CategoryCode and OrderInclude.ReferenceCode=" + id;
            ra=stmt3.executeQuery(sql3);
            if (!rs.next() ) {
                System.out.println("Order doesn't exist");
            } else {
                // Εκτύπωση των αποτελεσμάτων
                System.out.print("Reference Code: ");
                System.out.println(rs.getInt("ReferenceCode"));
                System.out.print("Order Date: ");
                System.out.println(rs.getString("OrderDate"));
                System.out.print("Shipping Date: ");
                System.out.println(rs.getString("Shipping"));
                System.out.print("Customer Code: ");
                System.out.println(rs.getInt("CustCode"));
                int n = 0;
                while (rb.next()) {
                    // Εκτύπωση των αποτελεσμάτων
                    n = n + 1 ;
                    System.out.println("\nInformations about Product #" + n );
                    System.out.print("Product Code: ");
                    System.out.println(rb.getString("Pcode"));
                    System.out.print("Quantity: ");
                    System.out.println(rb.getInt("Quantity"));
                    System.out.print("Price: ");
                    System.out.println(rb.getInt("Price"));
                    System.out.print("Name: ");
                    System.out.println(rb.getString("Name"));
                    System.out.print("Description: ");
                    System.out.println(rb.getString("Description"));
                    System.out.print("Type Code: ");
                    System.out.println(rb.getInt("CategoryCode"));
                    
                    //System.out.println(rs.getInt("Stock"));
                    if(ra.next()) {
                        System.out.print("Category Title: ");
                        System.out.println(ra.getString("Title"));
                        System.out.print("Category Description: ");
                        System.out.println(ra.getString("Description"));
                    }
                }
            }
            sc.close();
            rs.close();
            rb.close();
            ra.close();
            stmt.close();
            stmt2.close();
            stmt3.close();
            dbcon.close();
            } catch(SQLException e) {
                System.out.print("SQLException: ");
                System.out.println(e.getMessage());
            } finally {
            try {
                dbcon.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}

