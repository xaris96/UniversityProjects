<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<%@ page errorPage="error_ex3_8220210.jsp"%>
<% request.setCharacterEncoding("UTF-8"); %>

<!DOCTYPE html>
<html lang="en">
<head>
	<%@ include file="header_ex3_8220210.jsp" %>
	<meta name="description" content="3η Ατομική Άσκηση - register page">
	<title>3η Ατομική Άσκηση</title>
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
			<h1>Registration Form</h1>
		</div>
		<div class="alert alert-warning" role="alert" style="text-align: center; margin-bottom: 20px;">
			Please fill in the following form to create an account.
		</div>
		<form class="form-horizontal" action="registerController_ex3_8220210.jsp" method="post" >
			<div class="form-group row">
				<label for="Name" class="col-sm-3 control-label">Name</label>
				<div class="col-sm-6">
					<input type="text" class="form-control" id="Name" name="Name" placeholder="your name" required>
				</div>
			</div>

			<div class="form-group row" >
				<label for="Surname" class="col-sm-3 control-label">Surname</label>
				<div class="col-sm-6">
					<input type="text" class="form-control" id="Surname" name="Surname" placeholder="your surname" required>
				</div>
			</div>
			
			<div class="form-group row">
				<label for="Email" class="col-sm-3 control-label">Email</label>
				<div class="col-sm-6">
					<input type="email" class="form-control" id="Email" name="Email" placeholder="your email" required>
				</div>
			</div>

			<div class="form-group row">
				<label for="Username" class="col-sm-3 control-label">Username</label>
				<div class="col-sm-6">
					<input type="text" class="form-control" id="Username" name="Username" placeholder="your username" required>
				</div>
			</div>

			<div class="form-group row">
				<label for="Password" class="col-sm-3 control-label">Κωδικός:</label>
				<div class="col-sm-6">
					<input type="Password" class="form-control" id="Password" name="Password" placeholder="your Password" required>
				</div>
			</div>
			
			<div class="form-group row">
				<label for="confirmPassword" class="col-sm-3 control-label">Επιβεβαίωση Κωδικού:</label>
				<div class="col-sm-6">
					<input type="Password" class="form-control" id="confirmPassword" name="confirmPassword" placeholder="confirm your Password" required>
				</div>
			</div>
			<div class="form-group row">
				<div class="col-sm-offset-3 col-sm-6">
					<div class="checkbox">
						<label class="terms-label">
							<input type="checkbox" id="terms" name="terms" > I agree to the terms and conditions
					</label>
				</div>
			</div>
	</div>
			<div class="form-group row">
				<div class="col-sm-offset-3 col-sm-6">
					<div class="text-left">
						<button type="submit" class="btn btn-success">
							<span class="glyphicon glyphicon-ok"></span> Submit
						</button>
						<button type="button" class="btn btn-danger" onclick="window.history.back();">
							<span class="glyphicon glyphicon-remove"></span> Cancel
						</button>
					</div>
				</div>
			</div>
		</form>
	</div>
	<%@ include file="footer_ex3_8220210.jsp" %>
</body>
</html>
