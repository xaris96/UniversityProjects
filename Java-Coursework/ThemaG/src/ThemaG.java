import java.util.Scanner;
class ThemaG{
    public static void main(String args[]){
        int [][] table=new int[3][5];
        Scanner in=new Scanner(System.in);
        System.out.println("Eisagete tis bathmologies kathe foithth: ");
        for(int i=0;i<=2;i++){
            System.out.println("Bathmologies foithth noumero: "+(i+1));
            for (int j=0;j<=4;j++){
                    try{
                        table[i][j]=in.nextInt();
                    }
                    catch(Exception e){
                        System.err.print("Lathos typos eisagwghs, janaprospa8hse!!\n");
                        in.nextLine();
                        j-=1;
                    } 
            }
        }
        double avarageArray[]=new double[5];
        for(int i=0;i<=4;i++){
            avarageArray[i]=(table[0][i]+table[1][i]+table[2][i])/3;
        }
        for(int i=1;i<=5;i++){
            int stud_count=0;
            for(int j=0;j<=2;j++){
                if(table[j][i-1]>5){
                    stud_count++;
                }
            }
            System.out.println("Mesos oros mathimatos "+i+": "+avarageArray[i-1]+" kai o arithmos twn foithtwn pou egrapsan se auto panw apo 5 "+stud_count+":");
        }
    }
}
