<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page errorPage="error_ex2_8220210.jsp"%>
<%@ page import="java.util.List" %>
<%@ page import="exercise2_2024_2025_8220210.*" %>

<!DOCTYPE html>
<html lang="en">
    <head>
        <%@ include file="header_ex2_8220210.jsp" %>
        <meta name="description" content="2η Ατομική Άσκηση - about page">
        <title>2η Εργαστηριακη Άσκηση</title>
    </head>
    <style>
        .media-object {
            border: 2px solid #000; /* Add a border around the image */
            padding: 5px; /* Add some padding inside the border */
        }
    </style>
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
							<li><a href="index_ex2_8220210.jsp">Home</a></li>
							<li class="active"><a href="about_ex2_8220210.jsp">About</a></li>
						</ul>
						<ul class="nav navbar-nav navbar-right">
							<li><a href="register_ex2_8220210.jsp">Register</a></li>
							<li><a href="login_ex2_8220210.jsp">Sign in</a></li>
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
							<li><a href="index_ex2_8220210.jsp">Home</a></li>
							<li class="active"><a href="about_ex2_8220210.jsp">About</a></li>
							<li><a href="dashboard_ex2_8220210.jsp">Dashboard</a></li>
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
	<% } %>
            <div class="container theme-showcase" role="main">
                <div class="jumbotron">
                    <h1>ismgroup22</h1>
                </div>
                <div class="page-header">
                    <h1>Group Members</h1>
                </div>
                <div class="media">
                    <div class="media-left">
                        <img class="media-object" src="../images/member1.png" alt="Profile_Picture">
                    </div>
                    <div class="media-left media-middle">
                        <h4 class="media-heading"><strong>Student Name</strong> 8220210</h4>
                        <div class="media">
                            <img src="../images/mail.jpg" alt="email" style="width:25px;height:25px;">
                            <a href="#">student-portfolio</a>
                        </div>
                    </div>
                </div>
                <div class="media">
                    <div class="media-left">
                        <img class="media-object" src="../images/member1.png" alt="Profile_Picture">
                    </div>
                    <div class="media-left media-middle">
                        <h4 class="media-heading"><strong>Maria Eirini Sarmpani</strong> 8220133</h4>
                        <div class="media">
                            <img src="../images/mail.jpg" alt="email" style="width:25px;height:25px;">
                            <a href="#">teammate-one</a>
                        </div>
                    </div>
                </div>
                <div class="media">
                    <div class="media-left">
                        <img class="media-object" src="../images/member1.png" alt="Profile_Picture">
                    </div>
                    <div class="media-left media-middle">
                        <h4 class="media-heading"><strong>Maria Stephanaki</strong> 8220144</h4>
                        <div class="media">
                            <img src="../images/mail.jpg" alt="email" style="width:25px;height:25px;">
                            <a href="#">teammate-two</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
            <%@ include file="footer_ex2_8220210.jsp" %>
    </body>



</html>
