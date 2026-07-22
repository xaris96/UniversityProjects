<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page errorPage="error_ex3_8220210.jsp"%>
<%@ page import="java.util.List" %>
<%@ page import="exercise3_2024_2025_8220210.*" %>

<%
    User user = (User) session.getAttribute("userObj2024");
    if (user == null) {
        request.setAttribute("message", "You are not authorized to access this resource. Please login.");
        request.getRequestDispatcher("login_ex3_8220210.jsp").forward(request, response);
    } else {
        String username = request.getParameter("uname");
        UserDAO dao = new UserDAO();
        User foundUser = dao.findUser(username);
%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <%@ include file="header_ex3_8220210.jsp" %>
        <meta name="description" content="3η Ατομική Άσκηση - Dashboard">
        <title>3η Ατομική Άσκηση - Dashboard page</title>
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
                        <li><a href="about_ex3_8220210.jsp">About</a></li>
                        <li class="active"><a href="dashboard_ex3_8220210.jsp">Dashboard</a></li>
                    </ul>
                    <ul class="nav navbar-nav navbar-right">
                        <li>
                            <p class="navbar-text">Signed in as <%= user.getUsername() %></p>
                        </li>
                        <li>
                            <a href="logout_ex3_8220210.jsp"><span class="glyphicon glyphicon-log-out"></span> Sign out</a>
                        </li>
                    </ul>
                </div>
                <!--/.nav-collapse -->
            </div>
        </nav>
        <div class="container theme-showcase" role="main">
            <!-- Main jumbotron for a primary marketing message or call to action -->
            <div class="jumbotron">
                <h1>3η Ατομική Άσκηση</h1>
            </div>
            <!-- Page Title -->
        <% if (foundUser != null) {
            String firstname = foundUser.getFirstname();
            String lastname = foundUser.getLastname();
            String email = foundUser.getEmail();
        %>
            <div class="page-header">
                <h1>
                    Profile of:
                    <span class="text-danger bg-danger"><%= firstname %> <%= lastname %></span>
                </h1>
            </div>
            <ul class="list-unstyled">
                <li><strong>First Name:</strong> <%= firstname %></li>
                <li><strong>Last Name:</strong> <%= lastname %></li>
                <li><strong>Email:</strong> <%= email %></li>
                <li><strong>Username:</strong> <%= username %></li>
            </ul>
        <% } else { %>
            <div class="alert alert-danger text-center" role="alert">User not found!</div>
        <% } %>
        </div>
        <%@ include file="footer_ex3_8220210.jsp" %>
    
    </body>
</html>
<%
    }
%>

