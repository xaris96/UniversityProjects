<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page errorPage="error_ex2_8220210.jsp"%>
<%@ page import="java.util.List" %>
<%@ page import="exercise2_2024_2025_8220210.*" %>

<%
	User user = (User) session.getAttribute("userObj2024");
	if (user == null) {
		request.setAttribute("message", "You are not authorized to access this resource. Please login.");
        request.getRequestDispatcher("login_ex2_8220210.jsp").forward(request, response);
	} else {
		String username = user.getUsername();
        String fullname = user.getFirstname() + " " + user.getLastname();
        UserDAO dao = new UserDAO();
        List<User> users = dao.getUsers();
		
%>
<!DOCTYPE html>
<html lang="en">
	<head>
		<%@ include file="header_ex2_8220210.jsp" %>
		<meta name="description" content="2η Ατομική Άσκηση - Dashboard">
		<title>2η Ατομική Άσκηση - Dashboard page</title>
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
						<li><a href="index_ex2_8220210.jsp">Home</a></li>
						<li><a href="about_ex2_8220210.jsp">About</a></li>
						<li class="active"><a href="dashboard_ex2_8220210.jsp">Dashboard</a></li>
										
					</ul>
					<ul class="nav navbar-nav navbar-right">
                        <li>
							<p class="navbar-text">Signed in as <%= username %></p>
						</li>
						<li>
							<a href="logout_ex2_8220210.jsp"><span class="glyphicon glyphicon-log-out"></span> Sign out</a>
						</li>
					</ul>
				</div>
				<!--/.nav-collapse -->
			</div>
		</nav>
		<div class="container theme-showcase" role="main">
			<!-- Main jumbotron for a primary marketing message or call to action -->
			<div class="jumbotron">
				<h1>2η Ατομική Άσκηση</h1>
			</div>
			<!-- Page Title -->
			<div class="page-header">
				<h1>
					Welcome
					<span class="text-danger bg-danger"><%= fullname %></span>
				</h1>
			</div>
			
            <div class="row">
                <div class="col-xs-12">
                    <h2>Available Users <span class="badge"><%= users.size() %></span></h2>
                </div>
            </div>
			<table class="table table-bordered">
                <thead class="bg-info">
					<tr>
						<th>A/A</th>
						<th>Last Name</th>
						<th>First Name</th>
						<th>Email</th>
					</tr>
                </thead>
                <tbody>
                    <% int index = 1; %>
                    <% for (User u : users) { %>
                        <tr class="<%= u.getUsername().equals(user.getUsername()) ? "success" : "" %>">
                            <td><%= index++ %></td>
                            <td><%= u.getLastname() %></td>
                            <td><%= u.getFirstname() %></td>
                            <td><%= u.getEmail() %></td>
                        </tr>
                    <% } %>
                </tbody>
            </table>
		</div>
		<!-- /container -->
        <%@ include file="footer_ex2_8220210.jsp" %>
	</body>
</html>
<% } %>
