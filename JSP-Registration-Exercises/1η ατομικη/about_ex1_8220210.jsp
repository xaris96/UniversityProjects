<%@ page contentType="text/html; charset=UTF-8" language="java" %>
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
        <title>1η Εργαστηριακη Άσκηση</title>
        <link rel="stylesheet" href="../css/bootstrap.min.css">
        <link rel="stylesheet" href="../css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link href="../css/theme_8XXXXXX.css" rel="stylesheet">
    </head>
    <style>
        .media-object {
            border: 2px solid #000; /* Add a border around the image */
            padding: 5px; /* Add some padding inside the border */
        }
    </style>
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
                            <li><a href="register_ex1_8220210.jsp">Register</a></li>
                            <li class="active"><a href="about_ex1_8220210.jsp">About</a></li>
                        </ul>
            
                    </div>
                    <!--/.nav-collapse -->
                </div>
            </nav>
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
            <footer class="navbar navbar-inverse navbar-fixed-bottom">
                <div class="container text-center">
                    <p>&copy; Copyright 2018 by ismgroup22</p>
                </div>
            </footer>
    </body>



</html>
