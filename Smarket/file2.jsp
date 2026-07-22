<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>

<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMARKET</title>
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
    <link rel="stylesheet" href="css/GeneralStyle.css">
</head>
<body>

    <div class="header">
        <img src="images/smarketlogo.png" alt="Supermarket Logo">
        <h1>Κατηγορίες Προϊόντων</h1>
        <div class="top-right-icons">
            <div class="icon" onclick="toggleDropdown()">
                <img src="images/acc.png" alt="Profile Icon" width="30" height="30">
                <div class="dropdown-content" id="profileDropdown">
                    <a href="formCus.html">Επεξεργασία Προφίλ</a>
                    <a href="formOwner.html">Επεξεργασία Καταστήματος</a>
                    <a href="add.html">Καταχώρηση Προϊόντων</a>
                    <a href="index.html">Αποσύνδεση</a>
                </div>
            </div>
            <div class="icon" onclick="toggleCartSidebar()">
                <img src="images/cart.jpg" alt="Shopping Cart" width="30" height="30">
            </div>
        </div>
    </div>
<div class="cart-sidebar" id="cartSidebar">
    <span class="close-cart" onclick="toggleCartSidebar()">&times;</span>
    <h2>Το Καλάθι Σας</h2>
    <div class="cart-item">Προϊόν 1</div>
    <div class="cart-item">Προϊόν 2</div>
    <div class="cart-item">Προϊόν 3</div>
</div>
<div class="category-banner">
    <div class="category">
        <a href="underconstruction.html"><h2>Κατεψυγμένα</h2></a>
    </div>
    <div class="category">
        <a href="underconstruction.html"><h2>Αρτοποιήματα</h2></a>
    </div>
    <div class="category">
        <a href="underconstruction.html"><h2>Αλμυρά σνακς</h2></a>
    </div>
    <div class="category">
        <a href="underconstruction.html"><h2>Γλυκά σνακς</h2></a>
    </div>
    <div class="category">
        <a href="underconstruction.html"><h2>Χυμοί και Αναψυκτικά</h2></a>
    </div>
    <div class="category">
        <a href="underconstruction.html"><h2>Ζυμαρικά και Όσπρια</h2></a>
    </div>
    <div class="category">
        <a href="underconstruction.html"><h2>Είδη Καθαρισμού</h2></a>
    </div>
    <div class="category">
        <a href="underconstruction.html"><h2>Χαρτικά</h2></a>
    </div>
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
