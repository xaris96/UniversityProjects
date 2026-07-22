-- Replace with the target database name before running.
use YOUR_DB_NAME_HERE;
CREATE TABLE Category (
    CategoryCode INTEGER NOT NULL,
    Title CHAR(30),
    Description VARCHAR(300),
    PRIMARY KEY (CategoryCode)
);

CREATE TABLE Products (
    Pcode INTEGER NOT NULL,
    Name VARCHAR(120),
    DESCRIPTION VARCHAR(300),
    Price DECIMAL(10,2),
    Stock INTEGER,
    CategoryCode INTEGER NOT NULL FOREIGN KEY REFERENCES Category,
    PRIMARY KEY (Pcode)
);

CREATE TABLE Region(
    GeoCode INT NOT NULL PRIMARY KEY,
    Gname VARCHAR(300),
    Population INTEGER
);

CREATE TABLE Suppliers(
    Scode INTEGER,
    VAT INTEGER,
    Label CHAR,
    Street VARCHAR(150),
    Number INTEGER,
    City VARCHAR(30),
    Phone BIGINT,
    PostalCode INTEGER,
    GeoCode INTEGER NOT NULL FOREIGN KEY REFERENCES Region,
    PRIMARY KEY (Scode)
);

CREATE TABLE Purchases (
    Tcode INTEGER NOT NULL PRIMARY KEY,
    Scode INTEGER NOT NULL FOREIGN KEY REFERENCES Suppliers,
    Date DATETIME,
    Quantity INTEGER NOT NULL,
    Pcode INTEGER NOT NULL FOREIGN KEY REFERENCES Products
);


CREATE TABLE Customers(
    CustCode INTEGER NOT NULL PRIMARY KEY,
    CusName VARCHAR(30),
    CusVAT INTEGER,
    Street VARCHAR(150),
    Number INTEGER,
    City VARCHAR(30),
    PostalCode INTEGER,
    GeoCode INTEGER NOT NULL FOREIGN KEY REFERENCES Region,
    CusPhone BIGINT
);

CREATE TABLE Special_Customers(
    CustCode INTEGER NOT NULL PRIMARY KEY,
    CreditLimit DECIMAL(10,2),
    AccBalance DECIMAL(10,2),
    FOREIGN KEY (CustCode) REFERENCES Customers(CustCode)
);

CREATE TABLE Specialpayments(
    Date DATE,
    Time TIME NOT NULL,
    Amount DECIMAL (10,2),
    CustCode INTEGER NOT NULL FOREIGN KEY REFERENCES Special_Customers
);

CREATE TABLE Orders(
    ReferenceCode INTEGER NOT NULL PRIMARY KEY,
    OrderDate DATE,
    Shipping DATE,
    CustCode INTEGER NOT NULL FOREIGN KEY REFERENCES Customers
);

CREATE TABLE OrderInclude(
    ReferenceCode INTEGER NOT NULL FOREIGN KEY REFERENCES Orders,
    Pcode INTEGER NOT NULL FOREIGN KEY REFERENCES Products,
    Quantity DECIMAL(10,2)
);
