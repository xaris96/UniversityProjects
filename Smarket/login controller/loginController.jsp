<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="smarket.*" %>
<%@ page import="java.util.ArrayList" %>

<%
    request.setCharacterEncoding("UTF-8");
    String username = request.getParameter("username");
    String password = request.getParameter("password");
    CustomerDAO dao = new CustomerDAO();
    Shop_AgentDAO dao2 = new Shop_AgentDAO();
    try {
        // Προσπάθεια σύνδεσης ως καταναλωτής
        Customer customer = dao.authenticate(username, password);
        if (customer != null) {
            session.setAttribute("customer", customer);
            session.setAttribute("role", "customer");
            response.sendRedirect("dashboard.jsp");
        } else {
            // Προσπάθεια σύνδεσης ως πωλητής
            Shop_Agent agent = dao2.authenticate(username, password);
            if (agent != null) {
                session.setAttribute("agent", agent);
                session.setAttribute("role", "agent");
                response.sendRedirect("dashboard_Agent.jsp");
            } else {
                // Σε περίπτωση αποτυχίας σύνδεσης, ορισμός μηνύματος στο request
                request.setAttribute("message", "Λάθος στοιχεία σύνδεσης");
                request.getRequestDispatcher("login.jsp").forward(request, response);
            }
        }
    } catch (Exception e) {
        // Σε περίπτωση σφάλματος, ορισμός μηνύματος στο request
        request.setAttribute("message", "Σφάλμα κατά την προσπάθεια σύνδεσης: " + e.getMessage());
        request.getRequestDispatcher("login.jsp").forward(request, response);
    }
%>

