package exercise2_2024_2025_8220210;

import java.util.ArrayList;
import java.util.List;

/**
 * UserService provides all the necessary methods related to users.
 * In future lesson we will change the code in order to provide data from a Database.
 *  
 * @version 1.0
 */
public class UserDAO {

    /**
	 * This method returns a List with all Users
	 * 
	 * @return List<User>
	 */
	public List<User> getUsers() {

		List<User> users = new ArrayList<User>();
		
		// adding some users for the sake of the example
		users.add(new User("Demo", "User One", "demo-user-1", "demo-user-1", "demo-pass-1"));
		users.add(new User("Demo", "User Two", "demo-user-2", "demo-user-2",  "demo-pass-2"));
        users.add(new User("Demo", "User Three", "demo-user-3", "demo-user-3",  "demo-pass-3"));
		
		return users;

	} //End of getUsers

    /**
	 * This method is used to authenticate a user.     
	 * 
	 * @param username, String the username
	 * @param password, String the password
	 * @return User, the User Object 
	 * @throws Exception, if the credentials are not valid or an error occurs.
	 */
    public User authenticate(String username, String password) throws Exception {
    
        List<User> users = getUsers();

		for (User user: users) {

			if (user.getUsername().equals(username) && user.getPassword().equals(password)) {
				return user; // credentials are valid, so return the User object
			}

		}
		//credentials are Wrong, so throw an error
		throw new Exception("Wrong username or password");

    } // End of authenticate

    
} //End of class
