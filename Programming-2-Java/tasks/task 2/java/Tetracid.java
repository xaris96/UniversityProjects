/*Άσκηση 17: Συναρτησιακός Προγραμματισμός

Άσκηση 1
Να γραφτεί μια κλάση με όνομα Tetracid. Η κλάση πρέπει να περιέχει
τις εξής μεθόδους:

1. Μια δημόσια ορατή μέθοδο με όνομα wasandawi, χωρίς όρισμα,
η οποία επιστρέφει ως αποτέλεσμα μια συνάρτηση (lambda function)
που δέχεται ως όρισμα μια τιμή τύπου Double και επιστρέφει την
τιμή αυτή πολλαπλασιασμένη με 12.

2. Μια δημόσια ορατή μέθοδο με όνομα rommack που δέχεται ένα όρισμα
τύπου Function<Integer, Integer> με όνομα π.χ. frize και επιστρέφει
αποτέλεσμα τύπου Function<Integer, Integer>. Η συνάρτηση (lambda
function) που επιστρέφεται θα πρέπει να παρέχει την τιμή της frize
μειωμένη κατά 56.

3. Μια δημόσια ορατή μέθοδο με όνομα papaship η οποία επιστρέφει
αποτέλεσμα τύπου Optional<Float> και δέχεται ως όρισμα τρία στοιχεία:
 - μια ροή (Stream) s τύπου Float,
 - ένα κατηγόρημα (Predicate) p για στοιχεία τύπου Float και
 - έναν δυαδικό τελεστή b για στοιχεία τύπου Float.
Η μέθοδος επιλέγει από τη ροή τα στοιχεία για τα οποία το p είναι
αληθές και επιστρέφει: αν υπάρχουν πάνω από ένα στοιχεία, το αποτέλεσμα
εφαρμογής του δυαδικού τελεστή b ανάμεσα στα στοιχεία για τα οποία
το p είναι αληθές (δηλ. α1 γ α2 γ α3 γ α4 γ), αλλιώς Optional<Float>.empty().
*/
import java.util.Optional;
import java.util.function.BinaryOperator;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;
public class Tetracid {
    public Function<Double, Double> wasandawi() {
        return x -> x * 12;
    }
    public Function<Integer, Integer> rommack(Function<Integer,
                                            Integer> frize) {
        return (Integer x) -> frize.apply(x) - 56;
    }
    public Optional<Float> papaship(Stream<Float> s, Predicate<Float> p,
                                    BinaryOperator<Float> b) {
        Stream<Float> z = s.filter(p);
        Optional<Float> result = z.reduce(b);
        return result;
    }
}

































































































































































































































































