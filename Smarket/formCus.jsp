<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>

<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Εγγραφή Καταναλωτή</title>
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
    <script>
        // Προσομοίωση υπαρχόντων ονομάτων χρηστών
        const existingUsernames = ["user123", "johnDoe", "janeDoe"];

        // Συνάρτηση για έλεγχο μοναδικότητας username
        function checkUsername() {
            const usernameInput = document.getElementById("username");
            const usernameError = document.getElementById("usernameError");

            if (existingUsernames.includes(usernameInput.value)) {
                usernameError.textContent = "Το όνομα χρήστη υπάρχει ήδη. Παρακαλώ επιλέξτε άλλο.";
                usernameInput.setCustomValidity("Το όνομα χρήστη δεν είναι διαθέσιμο");
            } else {
                usernameError.textContent = "";
                usernameInput.setCustomValidity("");
            }
        }
        // Συνάρτηση για έλεγχο πολυπλοκότητας κωδικού
        function checkPassword() {
            const passwordInput = document.getElementById("password");
            const passwordError = document.getElementById("passwordError");
            const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).{8,}$/;

            if (!passwordPattern.test(passwordInput.value)) {
                passwordError.textContent = "Ο κωδικός πρέπει να περιέχει τουλάχιστον ένα μικρό, ένα κεφαλαίο γράμμα, έναν αριθμό και ένα από τα σύμβολα !@#$%.";
                passwordInput.setCustomValidity("Ο κωδικός δεν πληροί τις απαιτήσεις ασφαλείας");
            } else {
                passwordError.textContent = "";
                passwordInput.setCustomValidity("");
            }
        }
    </script>
</head>
<body>

<header>
    <img src="images/smarketlogo.jpeg" alt="Supermarket Logo" class="logo">
    <h1>Εγγραφή Καταναλωτή</h1>
</header>

<main>
    <form id="registerCus" action="file2.html" method="POST">
        <h2>Στοιχεία Εγγραφής Καταναλωτή</h2>

        <label for="name">Όνομα:</label>
        <input type="text" id="name" name="name" required>

        <label for="surname">Επώνυμο:</label>
        <input type="text" id="surname" name="surname" required>

        <label for="address">Διεύθυνση:</label>
        <input type="text" id="address" name="address" required>

        <label for="zip">Ταχυδρομικός Κώδικας:</label>
        <input type="text" id="zip" name="zip" required>

        <label for="phone">Τηλέφωνο Επικοινωνίας:</label>
        <input type="text" id="phone" name="phone" required>

        <label for="email">E-mail:</label>
        <input type="email" id="email" name="email" required>

        <label for="preferences">Προτιμήσεις Προϊόντων και Καταστημάτων:</label>
        <textarea id="preferences" name="preferences"></textarea>

        <label for="username">Όνομα Χρήστη:</label>
        <input type="text" id="username" name="username" required oninput="checkUsername()">
        <span id="usernameError" style="color: red;"></span>

        <label for="password">Κωδικός Πρόσβασης:</label>
        <input type="password" id="password" name="password" required oninput="checkPassword()">
        <span id="passwordError" style="color: red;"></span>
        <div class="button-container">
            <button type="button" class="button back-button" onclick="window.location.href='register.html'">Επιστροφή</button>
            <button type="submit" class="button">Δημιουργία λογαριασμού</button>
        </div>
    </form>
</main>

</body>
</html>
