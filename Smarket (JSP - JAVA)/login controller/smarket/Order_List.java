package smarket;

public class Order_List {
    private int orderID;
    private double total;
    private int customerID;


    public Order_List(double total, int customerID) {
        this.total = total;
        this.customerID = customerID;
    }


    public Order_List(int orderID, double total, int customerID) {
        this.orderID = orderID;
        this.total = total;
        this.customerID = customerID;
    }


    public int getOrderID() {
        return orderID;
    }

    public void setOrderID(int orderID) {
        this.orderID = orderID;
    }

    public double getTotal() {
        return total;
    }

    public void setTotal(double total) {
        this.total = total;
    }

    public int getCustomerID() {
        return customerID;
    }

    public void setCustomerID(int customerID) {
        this.customerID = customerID;
    }
}
