import java.util.Scanner;
public class Main {
	

	public static void main(String[] args) {
		
		Scanner sc = new Scanner(System.in);
		
		BoardingPass bp = new BoardingPass();
		int z;
		int answer;
		
		do {
			System.out.println("Παρακαλώ πατήστε 1 για Πρώτη θέση ή 2 για Οικονομική θέση");
			answer = sc.nextInt(); //no value check asked
			if (answer==1) {
				z= bp.checkhighSeats();
			}else if (answer==2){
				z= bp.checklowSeats();
			}else {
				break; //in case of different answer the programm is terminated
			}
			if (z==0) {
				System.out.println("Η επόμενη πτήση είναι σε 3 ώρες");
			}else {
				System.out.println("Το Boarding pass επιβεβαιώθηκε στην θέση " + z);
			}
		}while (answer==1 || answer==2);
		System.out.println("Σας ευχαριστούμε για την προτίμηση!!");		
}
}
		
	
