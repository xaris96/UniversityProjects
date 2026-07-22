public class MainApp {
    public static void main(String[] args) {
        Unction unction = new Unction();
        try {
            UnctionResult result = unction.ionicize(42);
            System.out.println("Hostname: " + result.getHostname());
            System.out.println("Z: " + result.getZ());
        } catch (Exception e) {
            System.err.println("An error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
