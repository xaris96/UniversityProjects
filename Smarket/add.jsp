<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>


<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Καταχώρηση Νέου Προϊόντος</title>
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
</head>
<body>
    <h2>Καταχώρηση Νέου Προϊόντος</h2>
    <form action="/submit-product" method="post">
        <label for="name">Όνομα Προϊόντος:</label>
        <input type="text" id="name" name="name" required><br><br>

        <label for="brand">Μάρκα:</label>
        <input type="text" id="brand" name="brand"><br><br>

        <label for="description">Περιγραφή:</label>
        <textarea id="description" name="description"></textarea><br><br>

        <label for="price">Τιμή:</label>
        <input type="number" id="price" name="price" step="0.01" required><br><br>

        <label for="discount">Έκπτωση (%):</label>
        <input type="number" id="discount" name="discount" step="0.01" value="0"><br><br>

        <label for="supermarket">Σουπερμάρκετ:</label>
        <input type="text" id="supermarket" name="supermarket"><br><br>
        
        <label for="category">Κατηγορία:</label>
        
        <select id="category" name="category" required>
            <option value="Κατεψυγμένα">Κατεψυγμένα</option>
            <option value="Αρτοποιήματα">Αρτοποιήματα</option>
            <option value="Αλμυρά σνακς">Αλμυρά σνακς</option>
            <option value="Γλυκά σνακς">Γλυκά σνακς</option>
            <option value="Χυμοί και Αναψυκτικά">Χυμοί και Αναψυκτικά</option>
            <option value="Ζυμαρικά και Όσπρια">Ζυμαρικά και Όσπρια</option>
            <option value="Είδη Καθαρισμού">Είδη Καθαρισμού</option>
            <option value="Χαρτικά">Χαρτικά</option>
        </select><br><br>

        <label for="categoryDescription">Περιγραφή Κατηγορίας:</label>
        <textarea id="categoryDescription" name="categoryDescription"></textarea><br><br>
        <div class="button-container">
            <button type="button" class="button back-button" onclick="window.location.href='file2.html'">Επιστροφή</button>
            <button type="submit">Καταχώρηση Προϊόντος</button>
        </div>
        
    </form>
</body>
</html>
