<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>
<%@ page import="java.io.IOException" %>
<%@ page import="smarket.*" %>
<% 
    try {
        String categoryID = request.getParameter("categoryID");
        Category categ = new Category();
        Category mycateg = new Category();
        mycateg = categ.findCategory((int) "categoryID");
        
        session.setAttribute("categoryObj", mycateg);
        response.sendRedirect("categoryDashboard.jsp");
    
    } catch (Exception e){
        
        request.setAttribute("message", "Category not found");
        request.getRequestDispatcher("dashboard.jsp").forward(request, response);
    }
%>
 