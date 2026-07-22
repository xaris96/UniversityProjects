<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page import="smarket.*" %>
<%@ page import="java.util.List, java.util.ArrayList" %>
<%
    List<Category> categoryList;
    Category cat = new Category();
    try {
        categoryList = cat.getCategories2();
    } catch (Exception e) {
        e.printStackTrace();
        categoryList = new ArrayList();
    }
%>

<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Κατηγορίες Προϊόντων</title>
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <style>
        /* Προσαρμοσμένο CSS για κατηγορίες */
        .categories-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }

        .category {
            background-color: #fff5f7; /* Απαλό ροζ φόντο */
            border: 2px solid #ff3366; /* Έντονο ροζ πλαίσιο */
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 15px;
            width: 250px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .category:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        .category h3 {
            font-size: 1.3rem;
            margin: 10px 0;
            color: #ff3366; /* Έντονο ροζ για τίτλους */
            font-weight: bold;
        }

        .category p {
            font-size: 1rem;
            color: #333; /* Σκούρο γκρι για περιγραφές */
            line-height: 1.6;
        }

        .category form {
            margin: 0;
        }

        .category button {
            background-color: #ff3366;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 10px;
        }

        .category button:hover {
            background-color: #d12a5c;
        }
    </style>
</head>
<body>
<div class="header">
        <a href="intro.jsp">
            <img src="images/smarketlogo.jpeg" alt="Supermarket Logo" class="logo">
        </a>
        <h1>Κατηγορίες Προϊόντων</h1>
        <div class="top-right-icons">
            <div class="icon" onclick="toggleDropdown()">
                <img src="images/acc.png" alt="Profile Icon" width="30" height="30">
                <div class="dropdown-content" id="profileDropdown">
                    <a href="formCustomer.jsp">Επεξεργασία Προφίλ</a>
                    <a href="formAgent.jsp">Επεξεργασία Καταστήματος</a>
                    <a href="formProduct.jsp">Καταχώρηση Προϊόντων</a>
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
    <div class="categories-container">
        <%
        if (categoryList != null && !categoryList.isEmpty()) {
            for (Category category : categoryList) {
                int categoryID = category.getCategoryID();

        %>
        <div class="category">
            <form method="get" action="showProduct.jsp">
                <input type="hidden" name="supermarkedID" value="<%= category.getSupermarkedID()%>">
                <input type="hidden" name="categoryID" value="<%= category.getCategoryID()%>">
                <h3><%= category.getC_name() %></h3>
                <p><%= category.getDescription() %></p>
                <button type="submit">Προβολή προϊόντων</button>
            </form>
        </div>
        <%
            }
        } else {
        %>
            <p class="category">Δεν βρέθηκαν κατηγορίες προϊόντων.</p>
        <% } %>
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
