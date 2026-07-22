public class BoardingPass{
	public boolean [] seats;
	//create a matrix for our 10 seats
	public BoardingPass() {
		this.seats=new boolean[10];
		for (int i=0;i<10; i ++ ) {
			this.seats[i] = false;
		}
	}
	//Check for first line seats
	public int checkhighSeats() {
		for (int i=0;i<4;i++ ) {
			if (!(this.seats[i])==true) {
					this.seats[i]=true;
					return i+1;
			}
		}
		return 0;
	}
	
//Check for low fare seats
	public int checklowSeats() {
			
		for (int i=4;i<10;i++) {
			if (this.seats[i]==false) {
					this.seats[i]=true;
					return i+1;
								}
		}	
		return 0;
		
	}
}