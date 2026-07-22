package smarket;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * UserDAO provides all the necessary methods related to users.
 *
 * @author
 *
 */
public class Shop_AgentDAOtest {
	/**
	 * This method returns a List with all Users
	 *
	 * @return List<Shop_Agent>
	 */
	private static final String table = "shop_agent";
	public List<Shop_Agent> getUsers() throws Exception {
		List<Shop_Agent> users = new ArrayList<Shop_Agent>();
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
				Shop_Agent user = new Shop_Agent(rs.getString("name"), rs.getString("surname"), rs.getString("address"), rs.getString("zip"), rs.getString("phone"), rs.getString("email"), rs.getString("preferences"), rs.getString("username"), rs.getString("password"));
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
	public Shop_Agent findUser(String username) throws Exception {
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
				Shop_Agent user = new Shop_Agent(rs.getString("firstName"), rs.getString("lastName"), rs.getString("agentID"), rs.getString("email"), rs.getString("phone_number"), rs.getString("tax_code"), rs.getString("supermarketID"), rs.getString("username"), rs.getString("upassword"));
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
	public Shop_Agent authenticate(String username, String password) throws Exception {
		DB db = new DB();
		Connection conn = null;
		PreparedStatement ps = null;
		ResultSet rs = null;
		try {
			conn = db.getConnection();
			String query = "SELECT * FROM " + table + " WHERE username= ? AND upassword= ?";
			ps = conn.prepareStatement(query);
			ps.setString(1, username);
			ps.setString(2, password);
			rs = ps.executeQuery();
			if (rs.next()) {
				Shop_Agent user = new Shop_Agent(rs.getString( "firstName"), rs.getString("lastName"), rs.getString("agentID"), rs.getString("email"), rs.getString("phone_number"), rs.getString("tax_code"), rs.getString("supermarketID"), rs.getString("username"), rs.getString("upassword"));
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
	public void register(Shop_Agent user) throws Exception {
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
				query = "INSERT INTO " + table + " (username, name, surname, email, password) VALUES (?, ?, ?, ?, ?)";
				ps = conn.prepareStatement(query);
				ps.setString(1, user.getUsername());
				ps.setString(2, user.getname());
				ps.setString(3, user.getsurname());
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
