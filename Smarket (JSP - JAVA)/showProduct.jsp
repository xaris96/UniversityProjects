<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page import="smarket.*" %>
<%@ page import="java.util.List, java.util.ArrayList" %>
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Προϊόντα</title>
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <style>
        .products-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }

        .product {
            background-color: #fff5f7; /* Απαλό ροζ φόντο */
            border: 2px solid #ff3366; /* Έντονο ροζ πλαίσιο */
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 15px;
            width: 250px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .product:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        .product h3 {
            font-size: 1.3rem;
            margin: 10px 0;
            color: #ff3366; /* Έντονο ροζ για τίτλους */
            font-weight: bold;
        }

        .product p {
            font-size: 1rem;
            color: #333; /* Σκούρο γκρι για περιγραφές */
            line-height: 1.6;
        }

        .product form {
            margin: 0;
        }

        .product button {
            background-color: #ff3366;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 10px;
        }

        .product button:hover {
            background-color: #d12a5c;
        }
    </style>
</head>
<body>
<div class="header">
    <a href="intro.jsp">
        <img src="images/smarketlogo.jpeg" alt="Supermarket Logo" class="logo">
    </a>
    <h1>
        <%
            String categoryID = request.getParameter("categoryID");
            Category categ = null;
            CategoryDAO c2 = new CategoryDAO();
            String categoryName = ""; // Εξασφαλίζουμε ότι θα υπάρχει πάντα μια τιμή

            try {
                // Αν η κατηγορία απαιτεί ακέραιο αριθμό
                int categoryIDInt = Integer.parseInt(categoryID); // Μετατροπή σε int
                categ = c2.findCategory(categoryIDInt); // Εύρεση της κατηγορίας
                categoryName = categ.getC_name(); // Ανάκτηση του ονόματος της κατηγορίας
            } catch (Exception e) {
                categoryName = "Σφάλμα στην εύρεση κατηγορίας"; // Αν υπάρχει σφάλμα, εμφανίζεται ένα μήνυμα
            }

            // Εμφάνιση του ονόματος της κατηγορίας
            out.print(categoryName);
        %>
    </h1>
    <div class="top-right-icons">
        <div class="icon" onclick="toggleDropdown()">
            <img src="images/acc.png" alt="Profile Icon" width="30" height="30">
            <div class="dropdown-content" id="profileDropdown">
                <a href="formAgent.jsp">Επεξεργασία Καταστήματος</a>
                <a href="formProduct.jsp">Καταχώρηση Προϊόντων</a>
                <a href="logout.jsp">Αποσύνδεση</a>
            </div>
        </div>
    </div>
</div>

<div class="products-container">
    <%
        String supermarketID = request.getParameter("supermarkedID");

        if (supermarketID != null && categoryID != null) {
            ProductDAO dao = new ProductDAO();
            List<Product> products = new ArrayList();
            try {
                products = dao.getProductsByCategory(supermarketID, categoryID);
            } catch (Exception e) {
                e.printStackTrace();
            }
            if (products != null && !products.isEmpty()) {
                for (Product product : products) {
    %>
                    <div class="product">
                        <h3><%= product.getP_name() %></h3>
                        <p>Τιμή: <%= product.getPrice() %>€</p>
                        <form method="get" action="showProduct.jsp">
                            <input type="hidden" name="p_name" value="<%= product.getP_name() %>">
                            <button type="submit">Επεξεργασία Προϊόντος</button>
                        </form>
                    </div>
    <%
                }
            } else {
    %>
                <p>Δεν βρέθηκαν προϊόντα για την κατηγορία.</p>
    <%
            }
        } else {
    %>
            <p>Σφάλμα: Δεν παραλήφθηκαν οι απαραίτητες παράμετροι!</p>
    <%
        }
    %>
</div>

<script>
    function toggleDropdown() {
        var dropdown = document.getElementById("profileDropdown");
        dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    }
    window.onclick = function(event) {
        if (!event.target.matches('.icon img')) {
            var dropdown = document.getElementById("profileDropdown");
            if (dropdown && dropdown.style.display === "block") {
                dropdown.style.display = "none";
            }
        }
    }
</script>
</body>
</html>
