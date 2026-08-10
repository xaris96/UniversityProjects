package smarket;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;


public class CustomerDAO {


    public Customer findCustomer(int customerID) throws Exception {
        Connection con= null;
        PreparedStatement stmt = null;
        ResultSet rs = null;
        
        try {
            DB db = new DB();
            con = db.getConnection();

            String query = "SELECT customerID, firstName, lastName, c_adress, zipcode, phone_number, email, username, uPassword"+
            " FROM Customer WHERE customerID = ?";
            stmt = con.prepareStatement(query);
             
            stmt.setInt(1, customerID);

            rs = stmt.executeQuery();

            if (rs.next()) {
                String name = rs.getString("firstName");
                String surname = rs.getString("lastName");
                String address = rs.getString("c_adress");
                String zip = rs.getString("zipcode");
                String phone = rs.getString("phone_number");
                String email = rs.getString("email");
                String username = rs.getString("username");
                String password = rs.getString("uPassword");

                return new Customer(customerID, name, surname, address, zip, phone, email, username, password);
            } else {
                return null;
            }
            
    } catch (Exception e) {
        throw new Exception(e.getMessage(), e);
    } finally {
        if (rs != null) rs.close();
		if (stmt != null) stmt.close();
		if (con != null) con.close();
    }

}

public Customer authenticate(String username, String password) throws Exception {
    Connection con = null;
    PreparedStatement stmt = null;
    ResultSet rs = null;
    Customer user = null;
    try {
        DB db = new DB();
        con = db.getConnection();
        String query = "SELECT * FROM Customer WHERE username = ? AND uPassword = ?";
        stmt = con.prepareStatement(query);
        stmt.setString(1, username);
        stmt.setString(2, password);
        rs = stmt.executeQuery();
        if (rs.next()) {
            user = new Customer(
                rs.getInt("customerID"),
                rs.getString("firstName"),
                rs.getString("lastName"),
                rs.getString("c_adress"),
                rs.getString("zipcode"),
                rs.getString("phone_number"),
                rs.getString("email"),
                rs.getString("username"),
                rs.getString("uPassword")
            );
        } else {
            return null;
        }
    } catch (Exception e) {
        throw new Exception(e.getMessage());
    } finally {
        if (rs != null) rs.close();
        if (stmt != null) stmt.close();
        if (con != null) con.close();
    }
    
    return user;
}


public void register(Customer customer) throws Exception {
    Connection con = null;
    PreparedStatement stmt = null;
    ResultSet rs = null;

    try {
        DB db = new DB();
        con = db.getConnection();

        // Check if username or email already exists
        String checkQuery = "SELECT username FROM Customer WHERE username = ? OR email = ?";
        stmt = con.prepareStatement(checkQuery);
        stmt.setString(1, customer.getUsername());
        stmt.setString(2, customer.getEmail());

        rs = stmt.executeQuery();

        if (rs.next()) {
            throw new Exception("Sorry, username or email already registered");
        }

        // Insert the new customer into the database
        String insertQuery = "INSERT INTO Customer (firstName, lastName, c_adress, zipcode, phone_number, "
            + "email, username, uPassword) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        stmt = con.prepareStatement(insertQuery);
        stmt.setString(1, customer.getName());        // firstName
        stmt.setString(2, customer.getSurname());     // lastName
        stmt.setString(3, customer.getAddress());     // c_adress
        stmt.setString(4, customer.getZip());         // zipcode
        stmt.setString(5, customer.getPhone());       // phone_number
        stmt.setString(6, customer.getEmail());       // email
        stmt.setString(7, customer.getUsername());    // username
        stmt.setString(8, customer.getPassword());    // uPassword

        stmt.executeUpdate();  // Execute the insert

    } catch (Exception e) {
        throw new Exception(e.getMessage(), e);  // Propagate the exception
    } finally {
        // Close resources
        if (rs != null) rs.close();
        if (stmt != null) stmt.close();
        if (con != null) con.close();
    }	
}  

public void updateCustomer(Customer customer) throws Exception {

    DB db = new DB();
    Connection con = null;
    String sql = "UPDATE Customer SET firstName=?, lastName=?, c_adress=?, zipcode=?, " +
    "phone_number=?, email=?, username = ?, uPassword=? WHERE customerID=?";

    try {
        
        con = db.getConnection();
        PreparedStatement stmt = con.prepareStatement(sql);
       
        stmt.setInt(1, customer.getCustomerID());
        stmt.setString(2, customer.getName());
        stmt.setString(3, customer.getSurname());
        stmt.setString(4, customer.getAddress());
        stmt.setString(5, customer.getZip());
        stmt.setString(6, customer.getPhone());
        stmt.setString(7, customer.getEmail());
        stmt.setString(8, customer.getUsername());
        stmt.setString(9, customer.getPassword());
        
        stmt.executeUpdate();

        stmt.close();
        db.close();
        
    } catch (Exception e) {
        throw new Exception(e.getMessage());
    } finally {
        try {
         db.close();   
        } catch (Exception e) {
            
        }           
        
    }

}

}
