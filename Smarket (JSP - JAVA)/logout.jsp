<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<%@ page import="smarket.*" %>
<% request.setCharacterEncoding("UTF-8"); %>
<%
session.invalidate();
%>

<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <style>
        .alert {
            font-size: 1.5rem;
            font-weight: bold;
            color: #155724;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 15px;
            margin: 50px auto;
            text-align: center;
            max-width: 600px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .button-container {
            text-align: center;
            margin-top: 30px;
        }

        .back-button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 1.2rem;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        .back-button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }

        .back-button:active {
            transform: scale(1);
        }
    </style>
</head>
<body>
    <header>
        <div class="header">
            <a href="intro.jsp" class="button2">
                <img src="images/smarketlogo.jpeg" alt="Supermarket Logo" class="logo">
            </a>
        </div>
    </header>

    <div class="container theme-showcase" role="main">
        <div class="alert">Η έξοδος πραγματοποιήθηκε με επιτυχία</div>
        <div class="button-container">
            <button type="button" class="back-button" onclick="window.location.href='intro.jsp'">Αρχική Σελίδα</button>
        </div>
    </div>
</body>
</html>
