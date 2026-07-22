<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="Lab exercise template 2019-2020">
	<meta name="author" content="student-portfolio">
	<link rel="icon" href="../images/favicon.ico">
	<title>1η Ατομική Άσκηση</title>
	<link rel="stylesheet" href="../css/bootstrap.min.css">
	<link rel="stylesheet" href="../css/bootstrap-theme.min.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<link href="../css/theme_8XXXXXX.css" rel="stylesheet">
	<link rel="stylesheet" href="../css/extra.css">
	
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
			<h1>Registration Form</h1>
		</div>
		<div class="alert alert-warning" role="alert" style="text-align: center; margin-bottom: 20px;">
			Please fill in the following form to create an account.
		</div>
		<form class="form-horizontal" action="registerController_ex1_8220210.jsp" method="post" >
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
        <footer class="navbar navbar-inverse navbar-fixed-bottom">
            <div class="container text-center">
                <p>&copy; Copyright 2018 by ismgroup22</p>
            </div>
        </footer>
</body>
</html>
