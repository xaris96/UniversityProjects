package insurance;

public class Customer {
	public static int code;
	public static String nameC;
	public static int birthC;
	public static String sexC;
	public static Customer[] customerArray = new Customer[10];
	public static int customerCount = 0;

	public Customer(String name, int birth, String sex) {
		code = customerCount + 1;
		customerArray[customerCount] = this;
		nameC = name;
		birthC = birth;
		sexC = sex;
		customerCount++;
	}

	public int getCode() {
		return code;
	}

	public void setName(String name) {
		nameC = name;
	}

	public String getName() {
		return nameC;
	}

	public void setBirth(int birth) {
		birthC = (birth > 0 && birth < 140) ? birth : 0;
	}

	public int getBirth() {
		return birthC;
	}

	public void setSex(String sex) {
		sexC = sex;
	}

	public String getSex() {
		return sexC;
	}

	@Override
	public String toString() {
		return "\nCustomer:" + "code=" + code + "\nname=" + nameC + "\nage=" + birthC + "\nsex=" + sexC;
	}
}
