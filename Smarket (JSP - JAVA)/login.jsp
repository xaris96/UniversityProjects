<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<%@ page import="smarket.*" %>
<% request.setCharacterEncoding("UTF-8"); %>

<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <style>
        /* Προσθήκη στυλ για το μήνυμα λάθους */
        .alert-danger {
            
            padding: 20px;
            margin-bottom: 20px;
            
            border-radius: 8px; /* Στρογγυλεμένες γωνίες */
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Πιο απαλή σκιά */
            transition: all 0.3s ease-in-out; /* Ομαλή μετάβαση */
        }
        .alert-danger:hover {
            background-color: #c9302c; /* Σκούρο κόκκινο κατά την αλληλεπίδραση */
            border-color: #ac2925; /* Σκούρο κόκκινο border */
        }
    </style>
</head>
<body>
    <header>
        <div class="header">
            <a href="intro.jsp" class="button2">
                <img src="images/smarketlogo.jpeg" alt="Supermarket Logo" class="logo">
            </a>
            <h1 style="text-align: center;">Σύνδεση στο Smarket</h1>
        </div>
    </header>
    <div class="login-container">
        <% if(request.getAttribute("message") != null) { %>
                <div class="alert alert-danger text-center" role="alert"><%=(String)request.getAttribute("message") %></div>
        <% } %>
        <form class="form-signin" method="post" action="loginController.jsp">
            <h2 class="form-signin-heading text-center">Please sign in</h2>
            <label for="inputusername" class="sr-only">Username</label>
            <input type="text" name="username" id="inputusername" class="form-control" placeholder="username" required>
            <label for="inputpassword" class="sr-only">Password</label>
            <input name="password" type="password" id="inputpassword" class="form-control" placeholder="password" required>
            <div class="button-container">
                <button type="button" class="button back-button" onclick="window.location.href='index.jsp'">Επιστροφή</button>
                <button type="submit" class="btn btn-lg btn-primary btn-block">Σύνδεση</button>
            </div>
        </form>
        <p>Δεν έχετε λογαριασμό; <a href="register.jsp" style="color: black;">Εγγραφή</a></p>
    </div>
    

</body>
</html>
