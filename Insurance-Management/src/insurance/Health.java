package insurance;

public class Health extends Insurance {
	protected int max;

	public Health(int investment, int customerCode, int duration) {
		super(customerCode, duration);
		this.max = investment;
	}

	public int getMax() {
		return max;
	}

	public void setMax(int max) {
		this.max = max;
	}

	@Override
	public int calculateCost() {
		int x = super.calculateCost() + (Customer.customerArray[customerCode - 1].getBirth() * 7);
		if (Customer.customerArray[customerCode - 1].getSex().equals("Male")) {
			x = x + 50;
		}
		return x;
	}

	@Override
	public String toString() {
		return "\nHealth Insurance:" + "\ncustomer ID=" + customerCode + "\nSecurityID=" + insuranceCode + "\nmax Expense=" + this.calculateCost();
	}
}
