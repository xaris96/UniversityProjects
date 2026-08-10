package insurance;

public class Insurance {
	protected int customerCode;
	protected int insuranceCode;
	protected double duration;
	protected static Insurance[] insuranceArray = new Insurance[10];
	protected static int insuranceCount = 0;

	public Insurance(int customerCode, int duration) {
		this.customerCode = customerCode;
		this.insuranceCode = insuranceCount + 1;
		this.duration = duration;
		insuranceArray[insuranceCount] = this;
		insuranceCount++;
	}

	public int calculateCost() {
		return 100;
	}

	@Override
	public String toString() {
		return "\nInsurance:" +
				"\ncustomerId=" + customerCode +
				"\n securityID=" + insuranceCode +
				"\n duration=" + duration;
	}

	public static void printAllInsurances(int x, int code) {
		if (x == 1) {
			for (int i = 0; i < insuranceCount; i++) {
				System.out.println(insuranceArray[i]);
			}
		} else if (x == 3) {
			System.out.println(Customer.customerArray[code - 1].toString());
			System.out.println(insuranceArray[code]);
		}
	}
}
