package insurance;

public class Life extends Insurance {
	protected int investment;

	public Life(int customerCode, int duration, int investment) {
		super(customerCode, duration);
		this.investment = investment;
	}

	@Override
	public int calculateCost() {
		return super.calculateCost() + 5 * Customer.birthC;
	}

	@Override
	public String toString() {
		if (this.investment > this.calculateCost()) {
			return "\nLife Insurance:\n" +
					"\ncustomerId=" + customerCode +
					"\n insuranceId=" + insuranceCode +
					"\n duration=" + duration +
					"\n investmentCapital=" + this.calculateCost();
		} else {
			return "\nNo enough investment for this insurance";
		}
	}
}
