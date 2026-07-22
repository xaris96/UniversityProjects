package smarket;

public class Shop_Agent {
    private int agentID;
    private String firstName;
    private String lastName;
    private String email;
    private String phone_number;
    private String username;
    private String uPassword;
    private String tax_code;
    private int supermarketID;

    public Shop_Agent(int agentID, String firstName, String lastName, String email, String phone_number, String username, String uPassword, String tax_code, int supermarketID) {
        this.agentID = agentID;
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.phone_number = phone_number;
        this.username = username;
        this.uPassword = uPassword;
        this.tax_code = tax_code;
        this.supermarketID = supermarketID;
    }
    // Getters and Setters

    public int getAgentID() {
        return agentID;
    }

    public void setAgentID(int agentID) {
        this.agentID = agentID;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone_number() {
        return phone_number;
    }

    public void setPhone_number(String phone_number) {
        this.phone_number = phone_number;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getuPassword() {
        return uPassword;
    }

    public void setuPassword(String uPassword) {
        this.uPassword = uPassword;
    }

    public String getTax_code() {
        return tax_code;
    }

    public void setTax_code(String tax_code) {
        this.tax_code = tax_code;
    }

    public int getSupermarketID() {
        return supermarketID;
    }

    public void setSupermarketID(int supermarketID) {
        this.supermarketID = supermarketID;
    }
}
