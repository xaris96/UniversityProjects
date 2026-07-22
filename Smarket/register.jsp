<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>

<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Εγγραφή στο Smarket</title>
    <link rel="icon" href="./images/smarketlogo.jpeg" type="image/x-icon">
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <style>
        .logo {
            cursor: pointer;
        }
    </style>
</head>
<body>

<header>
    <a href="index.html">
        <img src="images/smarketlogo.jpeg" alt="Supermarket Logo" class="logo">
    </a>
    <h1>Εγγραφή στο Smarket</h1>
</header>

<main>
    <section class="user-type-selection">
        <h2>Επιλέξτε Τύπο Χρήστη</h2>
        <a href="formCus.html" class="button">Καταναλωτής</a>
        <a href="formOwner.html" class="button">Εκπρόσωπος</a>
    </section>
</main>

</body>
</html>
