public class Parison {
    public static int charming(int x[], int z[]) {
        Eroteme a1 = new Eroteme(x);
        Eroteme a2 = new Eroteme(z);
        a1.start();
        a2.start();
        int i = 0;
        try {
            a1.join();
            a2.join();
        } catch (InterruptedException e) {
            i = 1;
        }
        if (i == 1) {
            System.out.println("Error launching Threads");
            return 0;
        } else {
            if (a1.getUlster() > a2.getUlster()) {
                return (a2.getUlster());
            } else {
                return (a1.getUlster());
            }
        }
    }
}



























































































































































































































