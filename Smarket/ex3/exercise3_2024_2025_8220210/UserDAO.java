package exercise3_2024_2025_8220210;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;


/**
 * UserDAO provides all the necessary methods related to users.
 *
 * @author
 *
 */
public class UserDAO {
	/**
	 * This method returns a List with all Users
	 *
	 * @return List<User>
	 */
	private static final String table = "users_ex3_8220210_2024_2025";
	public List<User> getUsers() throws Exception {
		List<User> users = new ArrayList<User>();
		Connection conn = null;
		PreparedStatement ps = null;
		ResultSet rs = null;
		
		DB db = new DB();
		try {
			conn = db.getConnection();
			String query = "SELECT * FROM " + table;
			ps = conn.prepareStatement(query);
			rs = ps.executeQuery();
			while (rs.next()) {
				User user = new User(rs.getString("firstname"), rs.getString("lastname"), rs.getString("email"), rs.getString("username"), rs.getString("password"));
				users.add(user);
			}
			return users;
		} catch (Exception e) {
			throw new Exception(e.getMessage());
		} finally {
			try {
				db.close();
			} catch (Exception e) {
			}
		}
	} //End of getUsers
	/**
	 * Search user by username
	 *
	 * @param username, String
	 * @return User, the User object or null
	 * @throws Exception
	 */
	public User findUser(String username) throws Exception {
		DB db = new DB();
		Connection conn = null;
		PreparedStatement ps = null;
		ResultSet rs = null;
		try {
			conn = db.getConnection();
			String query = "SELECT * FROM " + table + " WHERE username = ?";
			ps = conn.prepareStatement(query);
			ps.setString(1, username);
			rs = ps.executeQuery();
			if (rs.next()) {
				User user = new User(rs.getString("firstname"), rs.getString("lastname"), rs.getString("email"), rs.getString("username"), rs.getString("password"));
				return user;
			} else {
				return null;
			}
		} catch (Exception e) {
			throw new Exception(e.getMessage());
		} finally {
			try {
				db.close();
			} catch (Exception e) {
			}
		}
	}

	/**
	 * This method is used to authenticate a user.
	 *
	 * @param username, String
	 * @param password, String
	 * @return User, the User object
	 * @throws Exception, if the credentials are not valid
	 */
	public User authenticate(String username, String password) throws Exception {
		DB db = new DB();
		Connection conn = null;
		PreparedStatement ps = null;
		ResultSet rs = null;
		try {
			conn = db.getConnection();
			String query = "SELECT * FROM " + table + " WHERE username= ? AND password= ?";
			ps = conn.prepareStatement(query);
			ps.setString(1, username);
			ps.setString(2, password);
			rs = ps.executeQuery();
			if (rs.next()) {
				User user = new User(rs.getString("firstname"), rs.getString("lastname"), rs.getString("email"), rs.getString("username"), rs.getString("password"));
				return user;
			} else {
				throw new Exception("Wrong username or password");
			}
		} catch (Exception e) {
			throw new Exception(e.getMessage());
		} finally {
			try {
				db.close();
			} catch (Exception e) {
			}
		}
	} //End of authenticate
	/**
	 * Register/create new User.
	 *
	 * @param user, User
	 * @throws Exception, if encounter any error.
	 */
	public void register(User user) throws Exception {
		DB db = new DB();
		Connection conn = null;
		PreparedStatement ps = null;
		ResultSet rs = null;
		try {
			conn = db.getConnection();
			String query = "SELECT * FROM " + table + " WHERE username = ? OR email = ?";
			ps = conn.prepareStatement(query);
			ps.setString(1, user.getUsername());
			ps.setString(2, user.getEmail());
			rs = ps.executeQuery();
			if (rs.next()) {
				throw new Exception("Sorry, username or email already registered");
			} else {
				query = "INSERT INTO " + table + " (username, firstname, lastname, email, password) VALUES (?, ?, ?, ?, ?)";
				ps = conn.prepareStatement(query);
				ps.setString(1, user.getUsername());
				ps.setString(2, user.getFirstname());
				ps.setString(3, user.getLastname());
				ps.setString(4, user.getEmail());
				ps.setString(5, user.getPassword());
				ps.executeUpdate();
			}
		} catch (Exception e) {
			throw new Exception(e.getMessage());
		} finally {
			try {
				db.close();
			} catch (Exception e) {
			}
		}
	}

} //End of class
