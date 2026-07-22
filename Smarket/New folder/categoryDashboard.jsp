<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page import="smarket.*" %>
<%@ page import="java.util.List, java.util.ArrayList" %>
<%@ page import="java.util.Map, java.util.HashMap" %>
<%
    String categoryID = request.getParameter("categoryID");
    
    int categoryIDInt = 0;
    
    try {
        if (categoryID != null && !categoryID.isEmpty()) {
            categoryIDInt = Integer.parseInt(categoryID);
        } else {
            throw new IllegalArgumentException("Invalid categoryID");
        }
    } catch (NumberFormatException e) {
        e.printStackTrace();
        response.sendRedirect("dashboard.jsp?error=invalidCategory");
        return;
    } catch (IllegalArgumentException e) {
        e.printStackTrace();
        response.sendRedirect("dashboard.jsp?error=invalidCategory");
        return;
    }
    

    Category categ = null;
    
    try{
        categ = Category.findCategory(categoryIDInt);
        String categoryName = categ.getC_name();
    } catch (Exception e) {
        request.getAttribute("message");
    }

    List<Product> productList;
    List<Product> productListUn;
    try {
        productList = Product.getProducts(categoryIDInt);
        productListUn = Product.getUniqueProducts(productList);
    } catch (Exception e) {
        e.printStackTrace();
        productList = new ArrayList();
        productListUn = new ArrayList();
    }
%>
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%= categ.getC_name() %></title>
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
            border: 2px solid #eb4034; /* Έντονο ροζ πλαίσιο */
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
            color: #eb4034; /* Έντονο ροζ για τίτλους */
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
            background-color: #eb4034;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 10px;
        }

        .product button:hover {
            background-color: #ac2f26;
        }
    </style>
</head>
<body>
<% if (categ != null) {
%> 
    <div class="header">
        <a href="dashboard.jsp">
            <img src="images/smarketlogo.jpeg" alt="Supermarket Logo" class="logo">
        </a>
        <h1 style="text-align: center;"><%= categ.getC_name() %></h1>
        <div class="top-right-icons">
            <div class="icon" class="button2" onclick="toggleDropdown()">
                <img src="images/acc.png" alt="Profile Icon" width="30" height="30">
                <div class="dropdown-content" id="profileDropdown">
                    <a href="formCustomer.jsp">Επεξεργασία Προφίλ</a>
                    <a href="logout.jsp">Αποσύνδεση</a>
                </div>
            </div>
            <div class="icon">
                <a href="showCart.jsp">
                    <img src="images/cart.jpg" alt="Shopping Cart" width="30" height="30">
                </a>
            </div>
        </div>
    </div>

    <%
		if (request.getAttribute("message") != null) {
    %>
			<div class="alert alert-danger">

				<%=(String)request.getAttribute("message") %>

			</div>
    <%
		}
    %>

    <div class="products-container">
        <% 
        if (productListUn != null && !productListUn.isEmpty()) {
            for (Product product : productListUn) { 
        %>
        
            <div class="product">
                <h3><%= product.getP_name() %></h3>
                <form method="get" action="showProduct.jsp">
                    <input type="hidden" name="p_name" value="<%= product.getP_name() %>">
                    <button type="submit">Προσθήκη στο καλάθι</button>
                </form>
            </div>
        <% 
            } 
        } else { 
        %>
            <p class="products">Δεν βρέθηκαν προϊόντα για αυτήν την κατηγορία.</p>
        <% } %>
    </div>


    <script>
        function toggleDropdown() {
            var dropdown = document.getElementById("profileDropdown");
            dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
        }
        function toggleCartSidebar() {
            var sidebar = document.getElementById("cartSidebar");
            sidebar.classList.toggle("open");
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
<% } else {
    request.getAttribute("message");
} 
%>
</body>
</html>
