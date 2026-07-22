package insurance;
import java.util.Scanner;

public class InsuranceApp {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		Customer[] customerArray = new Customer[10];
		int choise;
		Insurance[] insuranceArray = new Insurance[10];
		int loop = 0;
		do {
			System.out.println("Please enter your name");
			String name = sc.nextLine();
			System.out.println("Please enter your gender");
			String sex = sc.nextLine();
			System.out.println("Please enter your age");
			int age = sc.nextInt();
			System.out.println("Please enter your duration");
			int duration = sc.nextInt();
			System.out.println("Please enter your max cost");
			int investment = sc.nextInt();
			do {
				System.out.println("------Menu---- \n1. Print all Insurances \n2. Insert customer's code to see his insurances \n3. Insert insurance code to see it's type");
				choise = sc.nextInt();
				sc.nextLine();
			} while (choise != 1 && choise != 2 && choise != 3 && choise != 0);
			if (choise == 0) {
				System.out.println("Invalid choice. Exiting the program.");
				break;
			}
			Customer customer = new Customer(name, age, sex);
			customer.setSex(sex);
			customer.setName(name);
			customer.setBirth(age);
			customerArray[customer.getCode() - 1] = customer;
			int customerCode = Customer.customerArray[customer.getCode() - 1].getCode();
			System.out.println("Choose the insurance you want: \n1)Life \n2) Health \n3) Both \n4) Nothing");
			int prefer = sc.nextInt();
			Insurance insurance = new Insurance(customerCode, duration);
			Life life = null;
			Health health = null;
			if (prefer == 1) {
				life = new Life(customerCode, duration, investment);
			} else if (prefer == 2) {
				health = new Health(investment, customerCode, duration);
			} else if (prefer == 3) {
				health = new Health(investment, customerCode, duration);
				life = new Life(customerCode, duration, investment);
			} else {
				prefer = 4;
			}

			if (loop == 0 && prefer == 4) {
				System.out.println("No insurances to print.");
			} else {
				if (choise == 1) {
					System.out.println("\nAll Insurances:");
					Insurance.printAllInsurances(choise, 0);
				} else if (choise == 2) {
					System.out.println("Enter customer's code");
					int code = sc.nextInt();
					System.out.println("\nInsurance:");
					System.out.println(insurance.insuranceArray[code - 1]);
				} else if (choise == 3) {
					System.out.println("Enter insurance's code");
					int code = sc.nextInt();
					System.out.println("\nInsurance:");
					Insurance.printAllInsurances(choise, code);
				} else {
					System.out.println("Wrong choise");
					sc.nextLine();
				}
			}
			if (prefer == 1 || prefer == 2 || prefer == 3) {
				loop = 1;
			}
		} while (choise != 0);
		sc.close();
	}
}
