## Παράρτημα Β: Ορισμοί Μεθοδολογίας και Παραδοχές

### 1. Πεδίο Ανάλυσης και Στόχος
Η ανάλυση απαντά στα 3 βασικά ερωτήματα:
1. Πόσο βαθιά καταναλώνουν οι χρήστες το περιεχόμενο ενός tour (Q1).
2. Αν η ακρόαση είναι ενεργητική ή παθητική (Q2).
3. Αν οι χρήστες ακολουθούν τη σειρά των stories ή κάνουν jump (Q3).

Όλοι οι δείκτες υπολογίζονται στα καθαρισμένα δεδομένα Ιουλίου-Οκτωβρίου 2025.

### 2. Σημειώσεις Δεδομένων και Περιορισμοί Καταγραφής
- Στο iOS το event `story_start` δεν καταγράφεται πάντα με συνέπεια.
- Για αυτό το Q3 δίνεται σε 2 εκδοχές:
  - **Strict**: Android + `story_start`.
  - **Proxy (cross-platform)**: Android + iOS με story-level proxy events.
- Στα mapping αρχεία δεν υπάρχει επίσημο πεδίο διάρκειας story.

### 3. Ορισμός Journey (`journey_idx`)
Ένα **journey** ορίζεται από το κλειδί:
- `user_key + tour_id + journey_idx`

Το `journey_idx` δημιουργείται με κανόνα χρονικού κενού:
- Ταξινομούμε τα events ανά `event_timestamp` μέσα σε κάθε `user_key + tour_id`.
- Αν το κενό μεταξύ 2 διαδοχικών events είναι **πάνω από 30 λεπτά**, ξεκινά νέο journey.

Σημαντικό:
- Το είδος event (π.χ. `story_listened_20/40/60/80`) δεν ανοίγει μόνο του νέο journey.
- Μόνο το χρονικό κενό επηρεάζει το split.

Παράδειγμα:
- Αν `story_listened_40` και `story_listened_60` απέχουν 35 λεπτά, ανήκουν σε διαφορετικά journeys.

### 4. Πότε Τελειώνει Ένα Journey
Ένα journey τελειώνει στο τελευταίο event πριν:
- από κενό >30 λεπτών, ή
- από το τέλος των διαθέσιμων δεδομένων για το συγκεκριμένο user-tour stream.

### 5. Πώς Ορίζεται το "Τέλος Tour" στο Q1
Το "τέλος tour" αξιολογείται ανά journey με canonical rank λογική:
1. Υπολογίζεται **canonical σειρά stories** ανά tour από median θέσεις παρατήρησης.
2. Βρίσκεται το `final_canonical_rank` (εκτιμώμενο τελευταίο rank story του tour).
3. Υπολογίζονται:
   - `reached_last_story`: μέγιστο rank που είδαμε >= `final_canonical_rank`
   - `reached_tour_end`: μέγιστο **end-like** rank >= `final_canonical_rank`

Το `end-like` rank μετρά μόνο stories με ισχυρή ένδειξη κατανάλωσης (depth >=80%).

Άρα στο Q1:
- `Reached tour end` = ισχυρή ένδειξη ότι έφτασε πραγματικά στο τέλος.
- `Abandoned before end` = δεν υπάρχει τέτοια ένδειξη.

Σε επίπεδο χρήστη:
- Χρήστης μετριέται ως "reached end" αν το πέτυχε σε **τουλάχιστον ένα** journey.

### 6. Ορισμοί Active / Passive (Q2)
Strong control events:
- `forward_10`, `backward_10`, `next_story`, `previous_story`, `click_progress_bar`

Ανά journey:
- `strong_control_events`: πλήθος strong controls.
- `controls_per_story = strong_control_events / stories_touched` (0 αν δεν υπάρχουν stories).

Κανόνας ταξινόμησης journey:
- **Active journey** αν:
  - `strong_control_events >= 2`, ή
  - `controls_per_story >= 0.2`
- **Passive journey** σε κάθε άλλη περίπτωση.

Γιατί `>=2` και όχι `>=1`:
- Μειώνει θόρυβο από τυχαίο/μεμονωμένο tap.
- Κρατά ένδειξη επαναλαμβανόμενης, συνειδητής αλληλεπίδρασης.

User-level labels:
- **Active only**: έχει active journeys, χωρίς passive.
- **Passive only**: δεν έχει κανένα active journey.
- **Mixed**: έχει και active και passive journeys.

### 7. Q3: Σειρά Stories vs Jumping
Για το order-following:
- Υπολογίζουμε `follows_common_order` (strict) ή `follows_common_order_proxy` (cross-platform).
- Βασίζεται σε μονοτονική πρόοδο των canonical ranks.

Για jump behavior:
- `has_jump_event` / `has_jump_event_proxy` είναι true όταν υπάρχει:
  - `previous_story`, `next_story`, `click_story`, `tour_item_clicked`

Σημαντική ερμηνεία:
- Το true/false του `follows_common_order` αθροίζει 100% μέσα στο δικό του metric.
- Το true/false του `has_jump_event` αθροίζει 100% μέσα στο δικό του metric.
- **Δεν αθροίζουμε** `follows_common_order % + has_jump_event %` μεταξύ τους, γιατί είναι διαφορετικές διαστάσεις συμπεριφοράς.

### 8. Time Metrics από `event_timestamp`
Με timestamps μπορούμε να υπολογίσουμε συμπεριφορικό χρόνο, αλλά όχι τέλεια πραγματική διάρκεια audio αρχείου.

Χρήσιμες έννοιες:
- **Elapsed time**: `max(timestamp) - min(timestamp)` σε story session ή journey.
- **Engaged time (proxy)**: άθροισμα event-to-event deltas με cap (π.χ. <=180 sec), ώστε να μειώνεται το idle/background inflation.

Επειδή δεν υπάρχει επίσημο πεδίο διάρκειας story, οι χρόνοι αντιμετωπίζονται ως behavioral proxies.

### 9. Τι Μπορεί να Αλλάξει τα Αποτελέσματα (Sensitivity)
Κύριοι μοχλοί ευαισθησίας:
- threshold split journey (30 vs 45/60 λεπτά),
- thresholds active ταξινόμησης (`>=2`, `0.2 controls/story`),
- threshold end-like evidence (σήμερα >=80%),
- strict vs proxy scope στο Q3.

Πρακτική σύσταση:
- Κρατάμε ένα baseline definition για τα επίσημα αποτελέσματα.
- Δίνουμε sensitivity checks στο παράρτημα για διαφάνεια και αξιοπιστία.
