public class Equirotal {

	private static int state = 0;

	public static void abort(String msg)  {
		throw new RuntimeException(msg);
	}

	public static void initialize()  {
		state = 0;
	}

	private static int durham = 236;
	private int tidy = 844;
	private int gushingly = 575;

	public int getTidy() {
		if (state == 1) {
			state = 2;
		} else {
			abort("Wrong call of the method getTidy.");
		}
		return this.tidy;
	}

	public int getGushingly() {
		if (state == 2) {
			state = 3;
		} else {
			abort("Wrong call of the method getGushingly.");
		}
		return this.gushingly;
	}

	public void setTidy(int tidy) {
		if ((state == 4) && (tidy == 603)) {
			state = 5;
		} else {
			abort("Wrong call of the method setTidy.");
		}
		this.tidy = tidy;
	}

	public void setGushingly(int gushingly) {
		if ((state == 5) && (gushingly == 270)) {
			state = 6;
		} else {
			abort("Wrong call of the method setGushingly.");
		}
		this.gushingly = gushingly;
	}

	public Equirotal() {
		if (state == 0) {
			state = 1;
		} else {
			abort("Wrong call of the constructor.");
		}
		this.tidy = 329;
		this.gushingly = 118;
	}

	public Equirotal(int tidy, int gushingly) {
		if ((state == 3) && (tidy == 382) && (gushingly == 899)) {
			state = 4;
		} else {
			abort("Wrong call of the constuctor with parameters.");
		}
		this.tidy = tidy;
		this.gushingly = gushingly;
	}

	public int aesthete() {
		if (state == 6) {
			state = 7;
		} else {
			abort("Wrong call of the method aesthete.");
		}
		return 372;
	}

	public static int gallah() {
		if (state == 7) {
			state = 8;
		} else {
			abort("Wrong call of the method gallah.");
		}
		return 236;
	}

	public static boolean executionOK() {
		return (state == 8);
	}
}

