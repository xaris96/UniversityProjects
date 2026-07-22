package smarket;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class CategoryDAO {
    public String getCategoryName(String categoryID) throws SQLException {
        DB db = new DB();
        Connection conn = null;
		PreparedStatement ps = null;
		ResultSet rs = null;
        try {
            conn = db.getConnection();
            String query = "SELECT name FROM category WHERE categoryID = ?";
            ps = conn.prepareStatement(query);
            ps.setString(1, categoryID);
            rs = ps.executeQuery();
            if (rs.next()) {
                return rs.getString("name");
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            db.close();
        }
        return null;
    }

    public ResultSet getProductsByCategory(String supermarketID, String categoryID) throws SQLException {
        DB db = new DB();
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        try {
            conn = db.getConnection();
            String query = "SELECT p_name, price FROM product WHERE supermarketID = ? AND categoryID = ?";
            ps = conn.prepareStatement(query);
            ps.setString(1, supermarketID);
            ps.setString(2, categoryID);
            rs = ps.executeQuery();
            return rs;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
}
