package smarket;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class CategoryService {
    private CategoryDAO categoryDAO = new CategoryDAO();

    public String fetchCategoryName(String categoryID) {
        try {
            return categoryDAO.getCategoryName(categoryID);
        } catch (SQLException e) {
            e.printStackTrace();
            return "Σφάλμα φόρτωσης";
        }
    }

    public List<Product> fetchProducts(String supermarketID, String categoryID) {
        List<Product> products = new ArrayList<Product>();
        try {
            ResultSet rs = categoryDAO.getProductsByCategory(supermarketID, categoryID);
            while (rs.next()) {
                Product product = new Product(rs.getString("p_name"), rs.getDouble("price"));
                products.add(product);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return products;
    }
}
