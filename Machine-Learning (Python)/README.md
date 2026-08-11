# Machine Learning, AI Ethics & Sustainability Analytics

Αυτό το φάκελος περιέχει τρία αυτόνομα και ολοκληρωμένα projects Μηχανικής Μάθησης, Στατιστικής Ανάλυσης και Επιστήμης Δεδομένων που εκπονήθηκαν κατά τη διάρκεια των σπουδών μου. Κάθε project εστιάζει σε διαφορετικό τομέα (Ηθική Τεχνητής Νοημοσύνης, Συμπεριφορική Οικονομική, Βιώσιμη Ανάπτυξη).

---

## Περιεχόμενα & Αναλυτική Περιγραφή Projects

### 1. `LLM_Age_Gender_Bias_Analysis.ipynb`
*   **Θεματική:** Αλγοριθμική Μεροληψία (Algorithmic Bias) & Ηθική Τεχνητής Νοημοσύνης.
*   **Τι κάνει:** Στατιστική μελέτη αναπαραγωγής (replication study) και εις βάθος διερεύνηση της επαγγελματικής μεροληψίας (occupational bias) ως προς την ηλικία και το φύλο στον διανυσματικό χώρο του μοντέλου **GPT-2 Large**. Επιπλέον, αναλύει πειραματικά δεδομένα (Treatment vs Control) για να αποδείξει το φαινόμενο ενίσχυσης της μεροληψίας (amplification effect) όταν οι χρήστες αλληλεπιδρούν με την αναζήτηση εικόνων (Google Images).
*   **Μεθοδολογία & Εργαλεία:** 
    *   `Python`, `Pandas`, `NumPy`
    *   `Statsmodels`: OLS Regression (neutral/baseline modeling), ANOVA (Sum coding, Type 2)
    *   `SciPy`: Pearson Correlation, Fisher transformation (95% CI), Welch's & One-sample T-tests
    *   `Altair` & `Seaborn`: Robustness Heatmaps, Interactive Scatter/Regression plots, KDE Density plots, Residuals analysis.

### 2. `Choices13k_Decision_Rate_Prediction.ipynb`
*   **Θεματική:** Μοντελοποίηση Συμπεριφοράς & Λήψη Αποφάσεων υπό Αβεβαιότητα (Behavioral Economics).
*   **Τι κάνει:** Πρόβλεψη του ποσοστού επιλογής (`bRate`) μεταξύ δύο οικονομικών λοταριών (A και B) σε 13.006 προβλήματα λήψης αποφάσεων (Choices13k dataset). Περιλαμβάνει εκτενές Feature Engineering τόσο για απόλυτα στατιστικά λοταρίας όσο και για συγκριτικά μεγέθη (B - A), ενσωματώνοντας ψυχομετρικούς μετασχηματισμούς Prospect Theory (`Psych_EV`).
*   **Μεθοδολογία & Εργαλεία:** 
    *   `Python`, `Scikit-learn`
    *   **Μοντέλα Μηχανικής Μάθησης:** `XGBoost` (Hist tree method / Pseudo-Huber loss), `Random Forest Regressor`, `Extra Trees Regressor`, `MLP Regressor` (Neural Network).
    *   **Αξιολόγηση & Tuning:** `GroupKFold` Cross-Validation (για αποφυγή data leakage μεταξύ προβλημάτων), Sample Weighting βάσει αξιοπιστίας/θορύβου (`bRate_std`), Random Search Hyperparameter Tuning, Bagged OOF Ensembling.
    *   **Ερμηνευσιμότητα (XAI):** Feature Importance, Permutation Importance, SHAP values.

### 3. `Global_Doughnut_Economics_Analysis.ipynb`
*   **Θεματική:** Ανάλυση Βιώσιμης Ανάπτυξης & Οικονομικά του Ντόνατ (Sustainability Analytics).
*   **Τι κάνει:** Επεξεργασία, οπτικοποίηση και ανάλυση της βιώσιμης ανάπτυξης σε παγκόσμιο επίπεδο (2000–2022) με βάση το πλαίσιο **Doughnut Economics** (Kate Raworth). Αντιπαραβάλλει την κάλυψη των βασικών ανθρώπινων αναγκών (Social Foundation) με την υπέρβαση των πλανητικών ορίων (Ecological Ceiling) και αναλύει την κατανομή ευθύνης/στερήσεων ανά εισοδηματική ομάδα (Bottom-40, Middle-40, Top-20).
*   **Μεθοδολογία & Εργαλεία:** 
    *   `Python`, `Pandas`, `NumPy`
    *   `Matplotlib` (Polar projections / ipympl): Ανάπτυξη custom διαδραστικών Doughnut Plots σε πολικές συντεταγμένες με δυναμικό χρωματικό scaling.
    *   `Seaborn`: Trellis / Facet Bar Charts για Ecological Overshoot και Social Shortfall (με ανεστραμμένους άξονες).
    *   Baguette / Sandwich Plots: Οπτικοποίηση ιστορικών τάσεων βελτίωσης ή επιδείνωσης ανά δείκτη.

---

## Notes & Security Practices
- **Self-Contained Notebooks:** Ο φάκελος περιέχει αποκλειστικά τα τελικά, αυτόνομα Notebooks[cite: 44]. Δοκιμαστικά σενάρια (test scripts), πρόχειρα notebooks και προσωρινοί φάκελοι ελέγχου έχουν αφαιρεθεί.
- **Privacy & Clean Codebase:** Πρωτογενή ερευνητικά δεδομένα, εξωτερικά CSV/JSON αρχεία και logs με αναγνωριστικά χρηστών/συμμετεχόντων έχουν αποκλειστεί (μέσω `.gitignore`) για λόγους προστασίας δεδομένων και ακαδημαϊκής δεοντολογίας[cite: 44].
- **Visualizations:** Τα διαγράμματα και τα αποτελέσματα των μοντέλων διατηρούνται ενσωματωμένα στον κώδικα των Notebooks μόνο όπου εξυπηρετούν την τεκμηρίωση της ανάλυσης[cite: 44].
