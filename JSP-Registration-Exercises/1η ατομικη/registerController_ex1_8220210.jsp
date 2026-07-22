<%@ page import="java.util.ArrayList" %>
<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<% request.setCharacterEncoding("UTF-8"); %>
<%
    String name = request.getParameter("Name");
    String surname = request.getParameter("Surname");
    String email = request.getParameter("Email");
    String username = request.getParameter("Username");
    String password = request.getParameter("Password");
    String confirmPassword = request.getParameter("confirmPassword");
    String terms = request.getParameter("terms");

    ArrayList<String> errors = new ArrayList<String>();

    if (name == null || name.length() < 3) {
        errors.add("Name must be at least 3 characters long");
    }
    if (surname == null || surname.length() < 3) {
        errors.add("Surname must be at least 3 characters long");
    }
    if (username == null || username.length() < 5) {
        errors.add("Username must be at least 5 characters long");
    }
    if (password == null || password.length() < 6) {
        errors.add("Password must be at least 6 characters long");
    }
    if (confirmPassword == null || !confirmPassword.equals(password)) {
        errors.add("Password and confirm do not match");
    }
    if (terms == null) {
        errors.add("You must agree to the terms and conditions");
    }

    if (errors.isEmpty()) {
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Registration almost done!</title>
    <link rel="stylesheet" href="../css/bootstrap.min.css">
	<link rel="stylesheet" href="../css/bootstrap-theme.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<link href="../css/theme_8XXXXXX.css" rel="stylesheet">
	<link rel="stylesheet" href="../css/extra8220210.css">
</head>
<body>
<!-- Fixed navbar -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span> <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">8220210</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="index_ex1_8220210.jsp">Home</a></li>
                    <li class="active"><a href="register_ex1_8220210.jsp">Register</a></li>
                    <li><a href="about_ex1_8220210.jsp">About</a></li>
                </ul>
    
            </div>
        </div>
    </nav>
	<div class="container theme-showcase" role="main">
		<div class="jumbotron">
			<h1>1η Ατομική Άσκηση</h1>
		</div>
		<div class="page-header">
			<h1>Registration almost done!</h1>
		</div>
        <div class="alert alert-success" role="alert">
            <p>Note: A verification link has been sent to the email: <%= email %></p>
        </div>
        <ul class="list-unstyled">
            <li><strong>Name:</strong> <%= name %></li>
            <li><strong>Surname:</strong> <%= surname %></li>
            <li><strong>Email:</strong> <%= email %></li>
            <li><strong>Username:</strong> <%= username %></li>
        </ul>
    </div>
    <footer class="navbar navbar-inverse navbar-fixed-bottom">
            <div class="container text-center">
                <p>&copy; Copyright 2018 by ismgroup22</p>
            </div>
    </footer>
</body>
</html>
<%
    } else {
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Registration form has errors</title>
	<link rel="stylesheet" href="../css/bootstrap.min.css">
	<link rel="stylesheet" href="../css/bootstrap-theme.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<link href="../css/theme_8XXXXXX.css" rel="stylesheet">
	<link rel="stylesheet" href="../css/extra8220210.css">
</head>
<body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span> <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">8220210</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="index_ex1_8220210.jsp">Home</a></li>
                    <li class="active"><a href="register_ex1_8220210.jsp">Register</a></li>
                    <li><a href="about_ex1_8220210.jsp">About</a></li>
                </ul>
            </div>
        </div>
    </nav>
	<div class="container theme-showcase" role="main">
		<div class="jumbotron">
			<h1>1η Ατομική Άσκηση</h1>
		</div>
		<div class="page-header">
			<h1>Registration form has errors</h1>
		</div>
    </div>
    <div class="container">
        <div class="alert alert-danger" role="alert">
            <ol>
                <% for (String error : errors) { %>
                    <li><%= error %></li>
                <% } %>
            </ol>
        </div>
        <a href="register_ex1_8220210.jsp" class="btn btn-primary">
            <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span> Back to the form
        </a>
    </div>
    
    <footer class="navbar navbar-inverse navbar-fixed-bottom">
            <div class="container text-center">
                <p>&copy; Copyright 2018 by ismgroup22</p>
            </div>
    </footer>
</body>
</html>
<%
    }
%>
