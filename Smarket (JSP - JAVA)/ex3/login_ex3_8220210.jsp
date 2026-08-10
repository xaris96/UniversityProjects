<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page errorPage="error_ex3_8220210.jsp"%>
<%@ page import="exercise3_2024_2025_8220210.*" %>

<!DOCTYPE html>
<html lang="en">
	<head>
		<%@ include file="header_ex3_8220210.jsp" %>
		<meta name="description" content="3η Ατομική Άσκηση - login">
		<title>3η Ατομική Άσκηση - login page</title>
		<style>
			.form-signin {
				max-width: 330px;
				padding: 15px;
				margin: 0 auto;
			}
			.form-signin .form-signin-heading,
			.form-signin .checkbox {
				margin-bottom: 10px;
			}
			.form-signin .form-control {
				position: relative;
				height: auto;
				-webkit-box-sizing: border-box;
				-moz-box-sizing: border-box;
				box-sizing: border-box;
				padding: 10px;
				font-size: 16px;
			}
			.form-signin .form-control:focus {
				z-index: 2;
			}
			.form-signin input[type="text"] {
				margin-bottom: 10px;
				border-bottom-right-radius: 0;
				border-bottom-left-radius: 0;
			
			}
			.form-signin input[type="password"] {
				margin-bottom: 10px;
				border-top-left-radius: 0;
				border-top-right-radius: 0;
			}
		</style>
	</head>
	
	<body>
		
		<div class="container" role="main">

            <% if(request.getAttribute("message") != null) { %>
                <div class="alert alert-danger text-center" role="alert"><%=(String)request.getAttribute("message") %></div>
            <% } %>
    
            <form class="form-signin" method="post" action="loginController_ex3_8220210.jsp">
                <h2 class="form-signin-heading text-center">Please sign in</h2>
                <label for="inputusername" class="sr-only">Username</label>
                <input type="text" name="username" id="inputusername" class="form-control" placeholder="username" required>
                <label for="inputpassword" class="sr-only">Password</label>
                <input name="password" type="password" id="inputpassword" class="form-control" placeholder="password" required>
    
                <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
            </form>
            <div class="alert alert-info"><strong>Help: </strong>
                    <ul>
                        <li>For Demo User One: demo-user-1 / demo-pass-1</li>
                        <li>For Demo User Two: demo-user-2 / demo-pass-2</li>
                        <li>For Demo User Three: demo-user-3 / demo-pass-3</li>
                    </ul>
            </div>
    
        </div>
		<!-- /container -->
        <%@ include file="footer_ex3_8220210.jsp" %>
	</body>
</html>
