package smarket;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class Shop_AgentDAO {
    private static final String table = "shop_agent";

    public List<Shop_Agent> getUsers() throws Exception {
        List<Shop_Agent> users = new ArrayList<Shop_Agent>();
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;

        DB db = new DB();
        try {
            conn = db.getConnection();
            String query = "SELECT * FROM " + table;
            ps = conn.prepareStatement(query);
            rs = ps.executeQuery();
            while (rs.next()) {
                Shop_Agent user = new Shop_Agent(
                    rs.getInt("agentID"),
                    rs.getString("firstName"),
                    rs.getString("lastName"),
                    rs.getString("email"),
                    rs.getString("phone_number"),
                    rs.getString("username"),
                    rs.getString("uPassword"),
                    rs.getString("tax_code"),
                    rs.getInt("supermarketID")
                );
                users.add(user);
            }
            return users;
        } catch (Exception e) {
            throw new Exception(e.getMessage());
        } finally {
            try {
                db.close();
            } catch (Exception e) {
            }
        }
    }

    public Shop_Agent findUser(String username) throws Exception {
        DB db = new DB();
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = db.getConnection();
            String query = "SELECT * FROM " + table + " WHERE username = ?";
            ps = conn.prepareStatement(query);
            ps.setString(1, username);
            rs = ps.executeQuery();
            if (rs.next()) {
                Shop_Agent user = new Shop_Agent(
                    rs.getInt("agentID"),
                    rs.getString("firstName"),
                    rs.getString("lastName"),
                    rs.getString("email"),
                    rs.getString("phone_number"),
                    rs.getString("username"),
                    rs.getString("uPassword"),
                    rs.getString("tax_code"),
                    rs.getInt("supermarketID")
                );
                return user;
            } else {
                return null;
            }
        } catch (Exception e) {
            throw new Exception(e.getMessage());
        } finally {
            try {
                db.close();
            } catch (Exception e) {
            }
        }
    }

    public Shop_Agent authenticate(String username, String password) throws Exception {
        DB db = new DB();
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = db.getConnection();
            String query = "SELECT * FROM " + table + " WHERE username= ? AND uPassword= ?";
            ps = conn.prepareStatement(query);
            ps.setString(1, username);
            ps.setString(2, password);
            rs = ps.executeQuery();
            if (rs.next()) {
                Shop_Agent user = new Shop_Agent(
                    rs.getInt("agentID"),
                    rs.getString("firstName"),
                    rs.getString("lastName"),
                    rs.getString("email"),
                    rs.getString("phone_number"),
                    rs.getString("username"),
                    rs.getString("uPassword"),
                    rs.getString("tax_code"),
                    rs.getInt("supermarketID")
                );
                return user;
            } else {
                throw new Exception("Wrong username or password<br>Please try again");
            }
        } catch (Exception e) {
            throw new Exception(e.getMessage());
        } finally {
            try {
                db.close();
            } catch (Exception e) {
            }
        }
    }
    

    public void register(Shop_Agent user) throws Exception {
        DB db = new DB();
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = db.getConnection();
            String query = "SELECT * FROM " + table + " WHERE username = ? OR email = ?";
            ps = conn.prepareStatement(query);
            ps.setString(1, user.getUsername());
            ps.setString(2, user.getEmail());
            rs = ps.executeQuery();
            if (rs.next()) {
                throw new Exception("User already exists");
            } else {
                query = "INSERT INTO " + table + " (firstName, lastName, email, phone_number, username, uPassword, tax_code, supermarketID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
                ps = conn.prepareStatement(query);
                ps.setString(1, user.getFirstName());
                ps.setString(2, user.getLastName());
                ps.setString(3, user.getEmail());
                ps.setString(4, user.getPhone_number());
                ps.setString(5, user.getUsername());
                ps.setString(6, user.getuPassword());
                ps.setString(7, user.getTax_code());
                ps.setInt(8, user.getSupermarketID());
                ps.executeUpdate();
            }
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
