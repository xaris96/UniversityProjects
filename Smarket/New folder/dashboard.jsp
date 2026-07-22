<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page import="smarket.*" %>
<%@ page import="java.util.List, java.util.ArrayList" %>
<%
    List<Category> categoryList;
    
    try {
        categoryList = Category.getCategories();
        
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

    
    <div class="category-banner">
        <% 
        if (categoryList != null && !categoryList.isEmpty()) {
            for (Category category : categoryList) {
                int categoryID = category.getCategoryID();
        %>
            <div class="category">
                <form method="get" action="categoryDashboard.jsp">
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
</body>
</html>
