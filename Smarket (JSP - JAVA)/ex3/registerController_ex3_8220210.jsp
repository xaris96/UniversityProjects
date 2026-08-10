<%@ page import="java.util.ArrayList" %>
<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<%@ page errorPage="error_ex3_8220210.jsp"%>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page import="exercise3_2024_2025_8220210.*" %>

<%
    String name = request.getParameter("Name");
    String surname = request.getParameter("Surname");
    String email = request.getParameter("Email");
    String username = request.getParameter("Username");
    String password = request.getParameter("Password");
    String confirmPassword = request.getParameter("confirmPassword");
    String terms = request.getParameter("terms");
    int count = 0;
    ArrayList<String> errors = new ArrayList<String>();

    try {
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
            UserDAO dao = new UserDAO();
            User user = new User(name, surname, email, username, password);
            dao.register(user);
    %>
<!DOCTYPE html>
<html lang="en">
<head>
    <%@ include file="header_ex3_8220210.jsp" %>
    <meta name="description" content="3η Ατομική Άσκηση - register controller page">
    <title>Registration almost done!</title>
    <link rel="stylesheet" href="<%=request.getContextPath() %>css/extra8220210.css">
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
                    <li><a href="index_ex3_8220210.jsp">Home</a></li>
                    <li class="active"><a href="register_ex3_8220210.jsp">Register</a></li>
                    <li><a href="about_ex3_8220210.jsp">About</a></li>
                </ul>
    
            </div>
        </div>
    </nav>
    <div class="container theme-showcase" role="main">
        <div class="jumbotron">
            <h1>3η Ατομική Άσκηση</h1>
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
    <%@ include file="footer_ex3_8220210.jsp" %>
</body>
</html>
    <%
        }
    } catch (Exception e) {
        errors.add(e.getMessage());
        count = 1;
    }
    if (!errors.isEmpty()) {
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <%@ include file="header_ex3_8220210.jsp" %>
    <meta name="description" content="3η Ατομική Άσκηση - register controller page">
    <title>Registration form has errors</title>
	<link rel="stylesheet" href="<%=request.getContextPath() %>css/extra8220210.css">
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
                    <li><a href="index_ex3_8220210.jsp">Home</a></li>
                    <li class="active"><a href="register_ex3_8220210.jsp">Register</a></li>
                    <li><a href="about_ex3_8220210.jsp">About</a></li>
                </ul>
            </div>
        </div>
    </nav>
	<div class="container theme-showcase" role="main">
		<div class="jumbotron">
			<h1>3η Ατομική Άσκηση</h1>
		</div>
		<div class="page-header">
			<h1>Registration form has errors</h1>
		</div>
    </div>
    <div class="container">
        <div class="alert alert-danger" role="alert">
            <% if (count == 0) { %>
                
            <ol>
                <% for (String error : errors) { %>
                    <li><%= error %></li>
                <% } %>
            </ol>
            <% } else { %>
                <ol><%= errors.get(0) %></ol>
            <% } %>
        </div>
        <a href="register_ex3_8220210.jsp" class="btn btn-primary">
            <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span> Back to the form
        </a>
    </div>
    <%@ include file="footer_ex3_8220210.jsp" %>
</body>
</html>
<%
    }
%>
