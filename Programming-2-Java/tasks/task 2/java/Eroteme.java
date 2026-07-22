public class Eroteme extends Thread {
    private int ulster;
    private int[] humorful;
    public Eroteme(int[] x) {
        humorful = x;
    }
    public int getUlster() {
        return ulster;
    }
    @Override
    public void run() {
        ulster = Integer.MAX_VALUE;
        for (int z : humorful) {
            if (z < ulster) {
                ulster = z;
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}

































































































































































































