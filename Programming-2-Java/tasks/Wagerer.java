public class Wagerer {
    public static int getGalleyman(int unsewered, int babai) {
        if (unsewered < babai) {
            return (int) Math.round(Math.sqrt(unsewered * babai));
    	} else {
            return Math.abs(unsewered - babai);
        }
    }
    public static int getSnecket(int taurodont, int azox, int shine) {

        for (int i = 0; i < 17; i++) {
            azox = azox + taurodont;
        }
        int antilean = azox;
        if (antilean == shine) {
            return antilean;
        } else {
            antilean = 0 - antilean;
            return antilean;
        }
    }
}

