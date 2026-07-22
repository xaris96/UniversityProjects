package smarket;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;


public class Category {
    private int categoryID;
    private String c_name;
    private String description;

    public Category() {
    }
    
    public Category(String c_name, String description) {
        this.c_name = c_name;
        this.description = description;
    }


    public Category(int categoryID, String c_name, String description) {
        this.categoryID = categoryID;
        this.c_name = c_name;
        this.description = description;
    }


    public int getCategoryID() {
        return categoryID;
    }

    public void setCategoryID(int categoryID) {
        this.categoryID = categoryID;
    }

    public String getC_name() {
        return c_name;
    }

    public void setC_name(String c_name) {
        this.c_name = c_name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public static Category findCategory(int categoryID) throws Exception {
        DB db = new DB();
        Connection con = null;
    
        // Define the SQL statement (to be executed)
        String sql = "SELECT * FROM Category WHERE categoryID=?;";
    
        
        Category categ = null;
    
        try {
            // open connection and get Connection object
            con = db.getConnection();
    
            PreparedStatement stmt = con.prepareStatement(sql);
    
            // set values to parameter
            stmt.setInt(1, categoryID);
    
            // execute the SQL statement (QUERY - SELECT) and get the results in a ResultSet)
            ResultSet rs = stmt.executeQuery();
    
            if (rs.next()) {
                categ = ( new Category(rs.getInt("categoryID"), 
                                    rs.getString("c_name"),
                                    rs.getString("description")) );
                
            }
            
             rs.close(); // closing ResultSet
            stmt.close(); // closing PreparedStatement
            db.close(); // closing connection
            
    
        } catch (Exception e) {
            throw new Exception(e.getMessage());
        } finally {
    
            try {
                 db.close();
            } catch (Exception e) {
    
            }
    
        }
    
    
        return categ;
        
    } //End of findCategory

    public List<Category> getCategories() throws Exception {
		DB db = new DB();
		Connection con = null;
		List<Category> categoryList = new ArrayList<>();
		// Define the SQL statement (to be executed)
		String sql = "SELECT * FROM Category;";
		


		try {

			// open connection and get Connection object
			con = db.getConnection();
			PreparedStatement stmt = con.prepareStatement(sql);
			
			// execute the SQL statement (QUERY - SELECT) and get the results in a ResultSet)
			ResultSet rs = stmt.executeQuery();

			while (rs.next()) {
				categoryList.add( new Category(rs.getInt("categoryID"),
                                            rs.getString("c_name"),
											rs.getString("description")));
                                            
			}

			rs.close(); // closing ResultSet
			stmt.close(); // closing PreparedStatement
			db.close(); // closing connection
			

		} catch (Exception e) {
			throw new Exception(e.getMessage());
        } finally {

			try {
			     db.close();
			} catch (Exception e) {

			}

		}
		return categoryList;
		
		
	} //End of getCategories
}