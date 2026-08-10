<%@ page import="java.util.Date, java.text.SimpleDateFormat" %>
<%@ page contentType="text/html; charset=UTF-8" language="java"%>
<% request.setCharacterEncoding("UTF-8"); %>

<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Καλωσόρισμα στο SMarket</title>
    <link rel="icon" href="./images/smarketlogo.png" type="image/x-icon">
    
    <link rel="stylesheet" href="css/GeneralStyle.css">
    <style>
        .intro-container {
    background-color: rgba(255, 255, 255, 0.8); /* Λευκό με 80% αδιαφάνεια */
    border-radius: 15px; /* Στρογγυλεμένες γωνίες */
    padding: 20px; /* Εσωτερικό περιθώριο */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Απαλή σκιά */
    max-width: 800px; /* Μέγιστο πλάτος */
    margin: 50px auto; /* Κέντρο στη σελίδα */
    text-align: center; /* Κέντρο το κείμενο */
}

.intro-container h1, .intro-container h2 {
    color: #333; /* Σκούρο γκρι για καλή αντίθεση */
    margin-bottom: 15px;
}

.intro-container p {
    color: #555; /* Ελαφρώς πιο ανοιχτό γκρι */
    line-height: 1.6; /* Βελτίωση αναγνωσιμότητας */
    margin-bottom: 20px;
}

.intro-container ul {
    list-style: disc; /* Κουκκίδες */
    margin: 0 auto 20px auto; /* Αυτόματο κέντρο */
    padding-left: 20px; /* Απόσταση από το κείμενο */
    text-align: left; /* Αριστερή στοίχιση */
    max-width: 500px; /* Περιορισμός πλάτους */
}

.button-container {
    margin-top: 20px;
}

.button {
    background-color: #007BFF; /* Μπλε χρώμα */
    color: white; /* Λευκό κείμενο */
    border: none;
    border-radius: 5px; /* Στρογγυλεμένες γωνίες */
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s ease; /* Ομαλή αλλαγή χρώματος */
}

.button:hover {
    background-color: #0056b3; /* Σκούρο μπλε στο hover */
}
</style>
</head>
<body>
    <header>
        <img src="./images/462561960_1267742214220930_4183437938919502299_n.png" alt="Smarket Logo" class="logo">
    </header>
    <div class="intro-container text-center">
        <h1>Καλως ήρθατε στο SMarket</h1>
        <p>
            Το <strong>SMarket</strong> είναι η πιο εύχρηστη πλατφόρμα για να οργανώσετε τα ψώνια σας από το σούπερ μάρκετ! Εισάγετε τα προϊόντα που θέλετε να αγοράσετε και δείτε σε ποιο σούπερ μάρκετ της περιοχής σας θα τα βρείτε στις χαμηλότερες τιμές.
        </p>
        <h2>Πώς Λειτουργεί:</h2>
        <ul>
            <li>Καταχωρίστε τη λίστα αγορών σας.</li>
            <li>Επιλέξτε την περιοχή σας.</li>
            <li>Ανακαλύψτε τις καλύτερες τιμές σε όλα τα διαθέσιμα σούπερ μάρκετ.</li>
        </ul>
        <p>
            Με το SMarket, εξοικονομείτε χρόνο και χρήματα ενώ κάνετε τις αγορές σας πιο εύκολες από ποτέ.
        </p>
        <div class="button-container">
            <button class="button" onclick="window.location.href='login.jsp'">Σύνδεση</button>
            <button class="button" onclick="window.location.href='register.jsp'">Εγγραφή</button>
        </div>
    </div>

</body>
</html>
