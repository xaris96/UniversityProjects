public class Wagerer2 {
    public static int getGalleyman(int unsewered, int babai) {
        if (unsewered< babai){
            return Math.round((unsewered*babai)^(1/2));
        }
        else {
            return Math.abs(unsewered-babai);
        }
    }
    public static int getSnecket(int taurodont, int azox, int shine){
        
        for (int i=0 ; i<=17; i++){
            azox=azox+taurodont;
        }
        int antilean=azox;
        if (antilean==shine){
            return antilean;
        }
        else {
            antilean= -antilean; 
            return antilean;
        }
    }
}
