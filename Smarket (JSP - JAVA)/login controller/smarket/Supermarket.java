package smarket;

public class Supermarket{
    private int supermarketID;
    private String brand_name;
    private String tax_code;
    private String s_adress;
    private String phone_number;

  
    public Supermarket(String brand_name, String tax_code, String s_adress, String phone_number) {
        this.brand_name = brand_name;
        this.tax_code = tax_code;
        this.s_adress = s_adress;
        this.phone_number = phone_number;
    }


    public Supermarket(int supermarketID, String brand_name, String tax_code, String s_adress, String phone_number) {
        this.supermarketID = supermarketID;
        this.brand_name = brand_name;
        this.tax_code = tax_code;
        this.s_adress = s_adress;
        this.phone_number = phone_number;
    }
    
    public int getSupermarketID() {
        return supermarketID;
     }

    public void setSupermarketID(int supermarketID) {
        this.supermarketID = supermarketID;
    }

    public String getTax_code() {
        return tax_code;
    }

    public void setTax_code(String tax_code) {
        this.tax_code = tax_code;
    }

    public String getS_adress() {
        return s_adress;
    }

    public void setS_adress(String s_adress) {
        this.s_adress = s_adress;
    }

    public String getPhone_number() {
        return phone_number;
    }

    public void setPhone_number(String phone_number) {
        this.phone_number = phone_number;
    }
    
}