<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page errorPage="error_ex2_8220210.jsp"%>
<%@ page import="exercise2_2024_2025_8220210.*" %>
<%@ page import="java.util.ArrayList" %>

<%
    request.setCharacterEncoding("UTF-8");
    String username = request.getParameter("username");
    String password = request.getParameter("password");
    UserDAO dao = new UserDAO();
    try {
        User userObj2024 = dao.authenticate(username, password);
        session.setAttribute("userObj2024", userObj2024);
        response.sendRedirect("dashboard_ex2_8220210.jsp");
            
    } catch (Exception e) {
        // Σε περίπτωση σφάλματος, ορισμός μηνύματος στο request
        request.setAttribute("message",  e.getMessage());
%>
        <jsp:forward page="login_ex2_8220210.jsp" />
<%
    }
%>
