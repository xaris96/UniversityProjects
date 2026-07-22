<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page errorPage="error_ex3_8220210.jsp"%>
<%@ page import="java.util.List" %>
<%@ page import="exercise3_2024_2025_8220210.*" %>

<!DOCTYPE html>
<html lang="en">
	<head>
		<%@ include file="header_ex3_8220210.jsp" %>
		<meta name="description" content="3η Ατομική Άσκηση - index page">
		<title>3η Εργαστηριακη Άσκηση</title>
	</head>
	<body>
		<%
		User user = (User) session.getAttribute("userObj2024");
		if (user == null) {
		%>
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
							<li class="active"><a href="index_ex3_8220210.jsp">Home</a></li>
							<li><a href="about_ex3_8220210.jsp">About</a></li>
						</ul>
						<ul class="nav navbar-nav navbar-right">
							<li><a href="register_ex3_8220210.jsp">Register</a></li>
							<li><a href="login_ex3_8220210.jsp">Sign in</a></li>
						</ul>
					</div>
					<!--/.nav-collapse -->
				</div>
			</nav>
	<%
		} else {
			String username = user.getUsername();
			String fullname = user.getFirstname() + " " + user.getLastname();
	%>
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
							<li class="active"><a href="index_ex3_8220210.jsp">Home</a></li>
							<li><a href="about_ex3_8220210.jsp">About</a></li>
							<li><a href="dashboard_ex3_8220210.jsp">Dashboard</a></li>
						</ul>
						<ul class="nav navbar-nav navbar-right">
							<li>
								<p class="navbar-text">Signed in as <%= username %></p>
							</li>
							<li>
								<a href="logout_ex3_8220210.jsp"><span class="glyphicon glyphicon-log-out"></span> Sign out</a>
							</li>
						</ul>
					</div>
					<!--/.nav-collapse -->
				</div>
			</nav>
	<% } %>
		<div class="container theme-showcase" role="main">
			<!-- Main jumbotron for a primary marketing message or call to action -->
			<div class="jumbotron">
				<h1>3η Ατομική Άσκηση</h1>
			</div>

			<!-- Page Title -->
			<div class="page-header">
				<h1>Student Name</h1>
				<h1>Maria Eirini Sarmpani</h1>
				<h1>Maria Stephanaki</h1>
			</div>
			
		</div>
		<!-- /container -->
		<%@ include file="footer_ex3_8220210.jsp" %>
	</body>
</html>
