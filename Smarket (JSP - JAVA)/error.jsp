<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page isErrorPage="true" %>


<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Error</title>
		<link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
		<link rel="stylesheet" href="css/GeneralStyle.css">
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
					<a class="navbar-brand" href="#">8220133</a>
				</div>
				<div id="navbar" class="navbar-collapse collapse">
					<ul class="nav navbar-nav">
						<li><a href="index_ex3_8220133.jsp">Home</a></li>
						<li><a href="about_ex3_8220133.jsp">About</a></li>
						<li><a href="dashboard_ex3_8220133.jsp">Dashboard</a></li>
										
					</ul>
					<ul class="nav navbar-nav navbar-right">
                        <li>
							<p class="navbar-text">Signed in as USERNAME</p>
						</li>
						<li>
							<a href="logout_ex3_8220133.jsp"><span class="glyphicon glyphicon-log-out"></span> Sign out</a>
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
			<div class="page-header">
				<h1>Oops something went wrong</h1>
			</div>
            <div class="row">
				<div class="col-xs-12">
					<h2>Description</h2>
					<% if(exception != null) { %>
						<p><code><%=exception %></code></p>
					<% } %>
				</div>
			</div>
		</div>
	</body>
</html>


