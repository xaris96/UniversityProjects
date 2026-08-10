package smarket;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;
import java.util.HashSet;


public class Product {
   private int productID; 
   private String p_name;
   private String description;
   private double price;
   private Double discount; 
   private int supermarketID;
   private int categoryID;

   
   public Product(String p_name, String description, double price, Double discount, int supermarketID, int categoryID) {
       this.p_name = p_name;
       this.description = description;
       this.price = price;
       this.discount = discount;
       this.supermarketID = supermarketID;
       this.categoryID = categoryID;
   }

 
   public Product(int productID, String p_name, String description, double price, Double discount, int supermarketID, int categoryID) {
       this.productID = productID;
       this.p_name = p_name;
       this.description = description;
       this.price = price;
       this.discount = discount;
       this.supermarketID = supermarketID;
       this.categoryID = categoryID;
   }


   public int getProductID() {
       return productID;
   }

   public void setProductID(int productID) {
       this.productID = productID;
   }

   public String getP_name() {
       return p_name;
   }

   public void setP_name(String p_name) {
       this.p_name = p_name;
   }

   public String getDescription() {
       return description;
   }

   public void setDescription(String description) {
       this.description = description;
   }

   public double getPrice() {
       return price;
   }

   public void setPrice(double price) {
       this.price = price;
   }

   public Double getDiscount() {
       return discount;
   }

   public void setDiscount(Double discount) {
       this.discount = discount;
   }

   public int getSupermarketID() {
       return supermarketID;
   }

   public void setSupermarketID(int supermarketID) {
       this.supermarketID = supermarketID;
   }

   public int getCategoryID() {
       return categoryID;
   }

   public void setCategoryID(int categoryID) {
       this.categoryID = categoryID;
   }



   public static List<Product> getProducts(int categoryID) throws Exception {
		DB db = new DB();
		Connection con = null;
		List<Product> productList = new ArrayList<>();
		// Define the SQL statement (to be executed)
		String sql = "SELECT * FROM Product WHERE categoryID=?;";
		


		try {

			// open connection and get Connection object
			con = db.getConnection();
			PreparedStatement stmt = con.prepareStatement(sql);
            stmt.setInt(1, categoryID);
			
			// execute the SQL statement (QUERY - SELECT) and get the results in a ResultSet)
			ResultSet rs = stmt.executeQuery();

			while (rs.next()) {
				productList.add( new Product(rs.getInt("productID"),
											rs.getString("p_name"),
											rs.getString("description"),
											rs.getDouble("price"),
											rs.getDouble("discount"),
                                            rs.getInt("supermarketID"),
                                            rs.getInt("categoryID")));
                                            
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
		return productList;
		
		
	} //End of getProducts


    public static List<Product> getUniqueProducts(List<Product> productList) throws Exception {
        
        List<Product> uniqueProducts = new ArrayList<>();
        
        HashSet<String> seenProductNames = new HashSet<>();
    
        for (Product product : productList) {
            
            if (!seenProductNames.contains(product.getP_name())) {
                
                seenProductNames.add(product.getP_name());
                
                uniqueProducts.add(product);
            }
        }
        
        return uniqueProducts;
    }
}
    
