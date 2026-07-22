package smarket;

public class Customer {
    private int customerID;
    private String name;
    private String surname;
    private String address;
    private String zip;
    private String phone;
    private String email;
    private String username;
    private String password;

    public Customer(int customerID, String name, String surname, String address, String zip, String phone, 
        String email, String username, String password) {
            this.customerID = customerID;
            this.name = name;
            this.surname = surname;
            this.address = address;
            this.zip = zip;
            this.phone = phone;
            this.email = email;
            this.username = username;
            this.password = password;

    }

    public Customer( String name, String surname, String address, String zip, String phone, 
    String email, String username, String password) {
        this.name = name;
        this.surname = surname;
        this.address = address;
        this.zip = zip;
        this.phone = phone;
        this.email = email;
        this.username = username;
        this.password = password;

}

    public int getCustomerID() {
        return customerID;
    }

    public void setCustomerID(int customerID) {
        this.customerID = customerID;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSurname() {
        return surname;
    }

    public void setSurname(String surname) {
        this.surname = surname;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getZip() {
        return zip;
    }

    public void setZip(String zip) {
        this.zip = zip;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone  = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}