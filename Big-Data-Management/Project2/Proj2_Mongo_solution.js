/*
Project #2 - MongoDB 
Run with:
mongosh Proj2_Mongo_solution.js
*/

use("shopnest");
db.dropDatabase();

const vendorIds = {
  v1: ObjectId("660000000000000000000001"),
  v2: ObjectId("660000000000000000000002"),
  v3: ObjectId("660000000000000000000003"),
  v4: ObjectId("660000000000000000000004")
};

const customerIds = {
  c1: ObjectId("661000000000000000000001"),
  c2: ObjectId("661000000000000000000002"),
  c3: ObjectId("661000000000000000000003"),
  c4: ObjectId("661000000000000000000004"),
  c5: ObjectId("661000000000000000000005"),
  c6: ObjectId("661000000000000000000006"),
  c7: ObjectId("661000000000000000000007"),
  c8: ObjectId("661000000000000000000008"),
  c9: ObjectId("661000000000000000000009"),
  c10: ObjectId("66100000000000000000000a")
};

const productIds = {
  p1: ObjectId("662000000000000000000001"),
  p2: ObjectId("662000000000000000000002"),
  p3: ObjectId("662000000000000000000003"),
  p4: ObjectId("662000000000000000000004"),
  p5: ObjectId("662000000000000000000005"),
  p6: ObjectId("662000000000000000000006"),
  p7: ObjectId("662000000000000000000007"),
  p8: ObjectId("662000000000000000000008"),
  p9: ObjectId("662000000000000000000009"),
  p10: ObjectId("66200000000000000000000a"),
  p11: ObjectId("66200000000000000000000b"),
  p12: ObjectId("66200000000000000000000c"),
  p13: ObjectId("66200000000000000000000d"),
  p14: ObjectId("66200000000000000000000e"),
  p15: ObjectId("66200000000000000000000f"),
  p16: ObjectId("662000000000000000000010"),
  p17: ObjectId("662000000000000000000011"),
  p18: ObjectId("662000000000000000000012"),
  p19: ObjectId("662000000000000000000013"),
  p20: ObjectId("662000000000000000000014")
};

const vendors = [
  {
    _id: vendorIds.v1,
    name: "Aegean Gadgets",
    email: "redacted-contact",
    country: "Greece",
    joined_at: ISODate("2024-02-10T00:00:00Z")
  },
  {
    _id: vendorIds.v2,
    name: "Northwind Books",
    email: "redacted-contact",
    country: "Germany",
    joined_at: ISODate("2023-11-19T00:00:00Z")
  },
  {
    _id: vendorIds.v3,
    name: "UrbanFit Apparel",
    email: "redacted-contact",
    country: "United Kingdom",
    joined_at: ISODate("2024-05-08T00:00:00Z")
  },
  {
    _id: vendorIds.v4,
    name: "HomeCraft Living",
    email: "redacted-contact",
    country: "France",
    joined_at: ISODate("2022-09-03T00:00:00Z")
  }
];

// Optional index for data quality in our custom vendors collection.
db.vendors.createIndex({ email: 1 }, { unique: true, name: "uniq_vendor_email" });

// Required index: unique SKU so every product code maps to one listing.
db.products.createIndex({ sku: 1 }, { unique: true, name: "uniq_product_sku" });
// Required by section 3 text search query ("wireless headphones").
db.products.createIndex(
  { name: "text", tags: "text", category: "text" },
  { name: "products_text_search" }
);
// Required index: customer order history lookups by time descending.
db.orders.createIndex(
  { customer_id: 1, created_at: -1 },
  { name: "orders_customer_created_desc" }
);
// Required index: dashboard filters by order status.
db.orders.createIndex({ status: 1 }, { name: "orders_status_idx" });

// Optional index for customer uniqueness.
db.customers.createIndex({ email: 1 }, { unique: true, name: "uniq_customer_email" });

db.vendors.insertMany(vendors);

const productSeed = [
  {
    _id: productIds.p1,
    sku: "SNT-1001",
    name: "Wireless Headphones Pro",
    category: "Electronics",
    vendor_id: vendorIds.v1,
    price: 89.9,
    stock: 120,
    ratings: { average: 4.6, count: 340 },
    tags: ["audio", "wireless", "featured", "new-arrival"],
    created_at: "2026-01-05T09:00:00Z"
  },
  {
    _id: productIds.p2,
    sku: "SNT-1002",
    name: "Wireless Earbuds Lite",
    category: "Electronics",
    vendor_id: vendorIds.v1,
    price: 49.9,
    stock: 200,
    ratings: { average: 4.2, count: 520 },
    tags: ["audio", "wireless", "sale"],
    created_at: "2026-01-08T10:00:00Z"
  },
  {
    _id: productIds.p3,
    sku: "SNT-1003",
    name: "4K Action Camera",
    category: "Electronics",
    vendor_id: vendorIds.v1,
    price: 129.0,
    stock: 75,
    ratings: { average: 4.1, count: 181 },
    tags: ["camera", "new-arrival"],
    created_at: "2026-01-11T11:00:00Z"
  },
  {
    _id: productIds.p4,
    sku: "SNT-1004",
    name: "Smartwatch Active",
    category: "Electronics",
    vendor_id: vendorIds.v1,
    price: 149.0,
    stock: 40,
    ratings: { average: 4.3, count: 260 },
    tags: ["wearable", "featured"],
    created_at: "2026-01-15T11:00:00Z"
  },
  {
    _id: productIds.p5,
    sku: "SNT-1005",
    name: "Bluetooth Speaker Mini",
    category: "Electronics",
    vendor_id: vendorIds.v1,
    price: 39.5,
    stock: 65,
    ratings: { average: 3.9, count: 300 },
    tags: ["audio", "clearance"],
    created_at: "2026-01-20T11:00:00Z"
  },
  {
    _id: productIds.p6,
    sku: "SNT-1006",
    name: "USB-C Charger 65W",
    category: "Electronics",
    vendor_id: vendorIds.v1,
    price: 29.9,
    stock: 300,
    ratings: { average: 4.5, count: 690 },
    tags: ["accessory", "sale", "featured"],
    created_at: "2026-01-21T11:00:00Z"
  },
  {
    _id: productIds.p7,
    sku: "SNT-1007",
    name: "Data Modeling with MongoDB",
    category: "Books",
    vendor_id: vendorIds.v2,
    price: 34.0,
    stock: 55,
    ratings: { average: 4.7, count: 120 },
    tags: ["database", "featured"],
    created_at: "2026-01-22T11:00:00Z"
  },
  {
    _id: productIds.p8,
    sku: "SNT-1008",
    name: "Modern Greek Cooking",
    category: "Books",
    vendor_id: vendorIds.v2,
    price: 22.5,
    stock: 30,
    ratings: { average: 4.4, count: 90 },
    tags: ["cooking", "new-arrival"],
    created_at: "2026-01-24T11:00:00Z"
  },
  {
    _id: productIds.p9,
    sku: "SNT-1009",
    name: "Sci-Fi Anthology 2026",
    category: "Books",
    vendor_id: vendorIds.v2,
    price: 18.9,
    stock: 18,
    ratings: { average: 4.1, count: 150 },
    tags: ["fiction", "sale"],
    created_at: "2026-01-26T11:00:00Z"
  },
  {
    _id: productIds.p10,
    sku: "SNT-1010",
    name: "Clean Code Patterns",
    category: "Books",
    vendor_id: vendorIds.v2,
    price: 41.2,
    stock: 25,
    ratings: { average: 4.8, count: 180 },
    tags: ["programming", "featured", "new-arrival"],
    created_at: "2026-01-28T11:00:00Z"
  },
  {
    _id: productIds.p11,
    sku: "SNT-1011",
    name: "Intro to Algorithms",
    category: "Books",
    vendor_id: vendorIds.v2,
    price: 37.0,
    stock: 12,
    ratings: { average: 3.8, count: 75 },
    tags: ["programming", "clearance"],
    created_at: "2026-01-29T11:00:00Z"
  },
  {
    _id: productIds.p12,
    sku: "SNT-1012",
    name: "Unisex Hoodie",
    category: "Clothing",
    vendor_id: vendorIds.v3,
    price: 45.0,
    stock: 90,
    ratings: { average: 4.0, count: 310 },
    tags: ["winter", "sale"],
    created_at: "2026-01-30T11:00:00Z"
  },
  {
    _id: productIds.p13,
    sku: "SNT-1013",
    name: "Running T-Shirt",
    category: "Clothing",
    vendor_id: vendorIds.v3,
    price: 27.5,
    stock: 150,
    ratings: { average: 4.2, count: 260 },
    tags: ["sports", "new-arrival", "featured"],
    created_at: "2026-02-01T11:00:00Z"
  },
  {
    _id: productIds.p14,
    sku: "SNT-1014",
    name: "Denim Jacket",
    category: "Clothing",
    vendor_id: vendorIds.v3,
    price: 79.0,
    stock: 20,
    ratings: { average: 4.4, count: 140 },
    tags: ["fashion", "featured"],
    created_at: "2026-02-02T11:00:00Z"
  },
  {
    _id: productIds.p15,
    sku: "SNT-1015",
    name: "Cotton Socks 5-Pack",
    category: "Clothing",
    vendor_id: vendorIds.v3,
    price: 12.99,
    stock: 500,
    ratings: { average: 4.1, count: 880 },
    tags: ["essentials", "clearance"],
    created_at: "2026-02-03T11:00:00Z"
  },
  {
    _id: productIds.p16,
    sku: "SNT-1016",
    name: "Air Fryer XL",
    category: "Home",
    vendor_id: vendorIds.v4,
    price: 119.9,
    stock: 35,
    ratings: { average: 4.5, count: 500 },
    tags: ["kitchen", "featured", "sale"],
    created_at: "2026-02-04T11:00:00Z"
  },
  {
    _id: productIds.p17,
    sku: "SNT-1017",
    name: "Ceramic Dinner Set",
    category: "Home",
    vendor_id: vendorIds.v4,
    price: 59.0,
    stock: 80,
    ratings: { average: 4.3, count: 220 },
    tags: ["kitchen", "new-arrival"],
    created_at: "2026-02-05T11:00:00Z"
  },
  {
    _id: productIds.p18,
    sku: "SNT-1018",
    name: "Desk Lamp Minimal",
    category: "Home",
    vendor_id: vendorIds.v4,
    price: 33.3,
    stock: 140,
    ratings: { average: 4.0, count: 430 },
    tags: ["lighting", "featured", "new-arrival"],
    created_at: "2026-02-06T11:00:00Z"
  },
  {
    _id: productIds.p19,
    sku: "SNT-1019",
    name: "Yoga Mat Pro",
    category: "Sports",
    vendor_id: vendorIds.v3,
    price: 25.9,
    stock: 95,
    ratings: { average: 4.6, count: 410 },
    tags: ["fitness", "featured"],
    created_at: "2026-02-07T11:00:00Z"
  },
  {
    _id: productIds.p20,
    sku: "SNT-1020",
    name: "Adjustable Dumbbell 20kg",
    category: "Sports",
    vendor_id: vendorIds.v3,
    price: 199.0,
    stock: 28,
    ratings: { average: 4.4, count: 190 },
    tags: ["fitness", "new-arrival", "sale"],
    created_at: "2026-02-08T11:00:00Z"
  }
];

const products = productSeed.map((p) => ({
  _id: p._id,
  sku: p.sku,
  name: p.name,
  category: p.category,
  vendor_id: p.vendor_id,
  price: NumberDecimal(p.price.toFixed(2)),
  stock: NumberInt(p.stock),
  ratings: {
    average: p.ratings.average,
    count: NumberInt(p.ratings.count)
  },
  tags: p.tags,
  created_at: ISODate(p.created_at)
}));

db.products.insertMany(products);

const customers = [
  {
    _id: customerIds.c1,
    email: "redacted-contact",
    name: "Customer One",
    address: { city: "Athens", country: "Greece" },
    tier: "gold",
    joined_at: ISODate("2024-01-10T00:00:00Z")
  },
  {
    _id: customerIds.c2,
    email: "redacted-contact",
    name: "Customer Two",
    address: { city: "Berlin", country: "Germany" },
    tier: "silver",
    joined_at: ISODate("2024-03-20T00:00:00Z")
  },
  {
    _id: customerIds.c3,
    email: "redacted-contact",
    name: "Customer Three",
    address: { city: "New York", country: "USA" },
    tier: "bronze",
    joined_at: ISODate("2025-01-05T00:00:00Z")
  },
  {
    _id: customerIds.c4,
    email: "redacted-contact",
    name: "Customer Four",
    address: { city: "Thessaloniki", country: "Greece" },
    tier: "silver",
    joined_at: ISODate("2024-08-12T00:00:00Z")
  },
  {
    _id: customerIds.c5,
    email: "redacted-contact",
    name: "Customer Five",
    address: { city: "Munich", country: "Germany" },
    tier: "gold",
    joined_at: ISODate("2023-12-15T00:00:00Z")
  },
  {
    _id: customerIds.c6,
    email: "redacted-contact",
    name: "Customer Six",
    address: { city: "Paris", country: "France" },
    tier: "bronze",
    joined_at: ISODate("2025-06-01T00:00:00Z")
  },
  {
    _id: customerIds.c7,
    email: "redacted-contact",
    name: "Customer Seven",
    address: { city: "Nicosia", country: "Cyprus" },
    tier: "gold",
    joined_at: ISODate("2024-11-03T00:00:00Z")
  },
  {
    _id: customerIds.c8,
    email: "redacted-contact",
    name: "Customer Eight",
    address: { city: "Tokyo", country: "Japan" },
    tier: "silver",
    joined_at: ISODate("2025-02-20T00:00:00Z")
  },
  {
    _id: customerIds.c9,
    email: "redacted-contact",
    name: "Customer Nine",
    address: { city: "Sofia", country: "Bulgaria" },
    tier: "bronze",
    joined_at: ISODate("2024-06-18T00:00:00Z")
  },
  {
    _id: customerIds.c10,
    email: "redacted-contact",
    name: "Customer Ten",
    address: { city: "London", country: "United Kingdom" },
    tier: "gold",
    joined_at: ISODate("2023-10-28T00:00:00Z")
  }
];

db.customers.insertMany(customers);

const productBySku = {};
for (const p of productSeed) {
  productBySku[p.sku] = p;
}

function makeItem(sku, qty) {
  const p = productBySku[sku];
  return {
    product_id: p._id,
    sku: p.sku,
    name: p.name,
    qty: NumberInt(qty),
    unit_price: NumberDecimal(p.price.toFixed(2))
  };
}

function makeOrder(orderSeed) {
  const items = orderSeed.lines.map(([sku, qty]) => makeItem(sku, qty));
  const totalCents = orderSeed.lines.reduce((sum, [sku, qty]) => {
    const priceCents = Math.round(productBySku[sku].price * 100);
    return sum + priceCents * qty;
  }, 0);

  return {
    _id: orderSeed._id,
    customer_id: orderSeed.customer_id,
    status: orderSeed.status,
    items: items,
    total: NumberDecimal((totalCents / 100).toFixed(2)),
    created_at: ISODate(orderSeed.created_at)
  };
}

const orderSeed = [
  {
    _id: ObjectId("663000000000000000000001"),
    customer_id: customerIds.c1,
    status: "delivered",
    created_at: "2026-01-12T10:00:00Z",
    lines: [["SNT-1001", 1], ["SNT-1006", 2]]
  },
  {
    _id: ObjectId("663000000000000000000002"),
    customer_id: customerIds.c1,
    status: "shipped",
    created_at: "2026-01-25T10:00:00Z",
    lines: [["SNT-1010", 1], ["SNT-1015", 4]]
  },
  {
    _id: ObjectId("663000000000000000000003"),
    customer_id: customerIds.c1,
    status: "delivered",
    created_at: "2026-02-03T10:00:00Z",
    lines: [["SNT-1013", 2], ["SNT-1019", 1]]
  },
  {
    _id: ObjectId("663000000000000000000004"),
    customer_id: customerIds.c1,
    status: "pending",
    created_at: "2026-02-18T10:00:00Z",
    lines: [["SNT-1016", 1]]
  },
  {
    _id: ObjectId("663000000000000000000005"),
    customer_id: customerIds.c1,
    status: "cancelled",
    created_at: "2026-03-02T10:00:00Z",
    lines: [["SNT-1020", 1]]
  },
  {
    _id: ObjectId("663000000000000000000006"),
    customer_id: customerIds.c1,
    status: "delivered",
    created_at: "2026-03-28T10:00:00Z",
    lines: [["SNT-1002", 2], ["SNT-1007", 1]]
  },
  {
    _id: ObjectId("663000000000000000000007"),
    customer_id: customerIds.c2,
    status: "delivered",
    created_at: "2026-01-15T10:00:00Z",
    lines: [["SNT-1003", 1], ["SNT-1006", 1]]
  },
  {
    _id: ObjectId("663000000000000000000008"),
    customer_id: customerIds.c2,
    status: "shipped",
    created_at: "2026-02-20T10:00:00Z",
    lines: [["SNT-1017", 1], ["SNT-1018", 2]]
  },
  {
    _id: ObjectId("663000000000000000000009"),
    customer_id: customerIds.c2,
    status: "cancelled",
    created_at: "2026-03-11T10:00:00Z",
    lines: [["SNT-1004", 1]]
  },
  {
    _id: ObjectId("66300000000000000000000a"),
    customer_id: customerIds.c2,
    status: "delivered",
    created_at: "2026-04-05T10:00:00Z",
    lines: [["SNT-1001", 1], ["SNT-1012", 1]]
  },
  {
    _id: ObjectId("66300000000000000000000b"),
    customer_id: customerIds.c3,
    status: "pending",
    created_at: "2026-01-19T10:00:00Z",
    lines: [["SNT-1008", 1], ["SNT-1009", 2]]
  },
  {
    _id: ObjectId("66300000000000000000000c"),
    customer_id: customerIds.c3,
    status: "delivered",
    created_at: "2026-02-27T10:00:00Z",
    lines: [["SNT-1016", 1], ["SNT-1017", 1]]
  },
  {
    _id: ObjectId("66300000000000000000000d"),
    customer_id: customerIds.c3,
    status: "shipped",
    created_at: "2026-03-30T10:00:00Z",
    lines: [["SNT-1015", 6]]
  },
  {
    _id: ObjectId("66300000000000000000000e"),
    customer_id: customerIds.c3,
    status: "cancelled",
    created_at: "2026-04-02T10:00:00Z",
    lines: [["SNT-1005", 2]]
  },
  {
    _id: ObjectId("66300000000000000000000f"),
    customer_id: customerIds.c4,
    status: "delivered",
    created_at: "2026-01-30T10:00:00Z",
    lines: [["SNT-1014", 1], ["SNT-1013", 1]]
  },
  {
    _id: ObjectId("663000000000000000000010"),
    customer_id: customerIds.c4,
    status: "shipped",
    created_at: "2026-03-06T10:00:00Z",
    lines: [["SNT-1006", 3]]
  },
  {
    _id: ObjectId("663000000000000000000011"),
    customer_id: customerIds.c4,
    status: "delivered",
    created_at: "2026-04-10T10:00:00Z",
    lines: [["SNT-1020", 1], ["SNT-1019", 1]]
  },
  {
    _id: ObjectId("663000000000000000000012"),
    customer_id: customerIds.c5,
    status: "delivered",
    created_at: "2026-02-09T10:00:00Z",
    lines: [["SNT-1007", 2], ["SNT-1010", 1]]
  },
  {
    _id: ObjectId("663000000000000000000013"),
    customer_id: customerIds.c5,
    status: "pending",
    created_at: "2026-03-14T10:00:00Z",
    lines: [["SNT-1018", 1], ["SNT-1015", 5]]
  },
  {
    _id: ObjectId("663000000000000000000014"),
    customer_id: customerIds.c5,
    status: "delivered",
    created_at: "2026-04-12T10:00:00Z",
    lines: [["SNT-1002", 1], ["SNT-1005", 1], ["SNT-1013", 2]]
  },
  {
    _id: ObjectId("663000000000000000000015"),
    customer_id: customerIds.c6,
    status: "cancelled",
    created_at: "2026-02-22T10:00:00Z",
    lines: [["SNT-1011", 1]]
  },
  {
    _id: ObjectId("663000000000000000000016"),
    customer_id: customerIds.c6,
    status: "delivered",
    created_at: "2026-03-21T10:00:00Z",
    lines: [["SNT-1003", 1], ["SNT-1019", 2]]
  },
  {
    _id: ObjectId("663000000000000000000017"),
    customer_id: customerIds.c7,
    status: "shipped",
    created_at: "2026-01-08T10:00:00Z",
    lines: [["SNT-1012", 2], ["SNT-1015", 3]]
  },
  {
    _id: ObjectId("663000000000000000000018"),
    customer_id: customerIds.c7,
    status: "delivered",
    created_at: "2026-03-25T10:00:00Z",
    lines: [["SNT-1016", 1], ["SNT-1006", 1]]
  },
  {
    _id: ObjectId("663000000000000000000019"),
    customer_id: customerIds.c8,
    status: "pending",
    created_at: "2026-02-14T10:00:00Z",
    lines: [["SNT-1008", 2], ["SNT-1017", 1]]
  },
  {
    _id: ObjectId("66300000000000000000001a"),
    customer_id: customerIds.c8,
    status: "delivered",
    created_at: "2026-04-01T10:00:00Z",
    lines: [["SNT-1001", 1], ["SNT-1002", 1], ["SNT-1006", 1]]
  },
  {
    _id: ObjectId("66300000000000000000001b"),
    customer_id: customerIds.c9,
    status: "cancelled",
    created_at: "2026-03-05T10:00:00Z",
    lines: [["SNT-1014", 1], ["SNT-1011", 1]]
  },
  {
    _id: ObjectId("66300000000000000000001c"),
    customer_id: customerIds.c9,
    status: "delivered",
    created_at: "2026-04-15T10:00:00Z",
    lines: [["SNT-1019", 1], ["SNT-1013", 3]]
  },
  {
    _id: ObjectId("66300000000000000000001d"),
    customer_id: customerIds.c10,
    status: "delivered",
    created_at: "2026-03-19T10:00:00Z",
    lines: [["SNT-1007", 1], ["SNT-1010", 1], ["SNT-1018", 1]]
  },
  {
    _id: ObjectId("66300000000000000000001e"),
    customer_id: customerIds.c10,
    status: "cancelled",
    created_at: "2026-04-16T10:00:00Z",
    lines: [["SNT-1020", 1], ["SNT-1004", 1]]
  }
];

const orders = orderSeed.map((o) => makeOrder(o));
db.orders.insertMany(orders);

print("=== Seed data inserted ===");
print("vendors:   " + db.vendors.countDocuments());
print("products:  " + db.products.countDocuments());
print("customers: " + db.customers.countDocuments());
print("orders:    " + db.orders.countDocuments());
print("cancelled orders: " + db.orders.countDocuments({ status: "cancelled" }));
print(
  "max orders by one customer: " +
    db.orders
      .aggregate([
        { $group: { _id: "$customer_id", n: { $sum: 1 } } },
        { $sort: { n: -1 } },
        { $limit: 1 }
      ])
      .toArray()[0].n
);

function insertProductSafe(product) {
  const previous = db.products.findOneAndUpdate(
    { sku: product.sku },
    { $setOnInsert: product },
    { upsert: true, returnDocument: "before" }
  );

  if (previous === null) {
    print("Inserted: " + product.sku);
  } else {
    print("Skipped (exists): " + product.sku);
  }
}

const duplicateTestProduct = {
  sku: "SNT-9999",
  name: "Test Widget",
  category: "Electronics",
  vendor_id: vendorIds.v1,
  price: NumberDecimal("19.99"),
  stock: NumberInt(10),
  ratings: { average: 4.0, count: NumberInt(1) },
  tags: ["test", "demo"],
  created_at: ISODate("2026-04-18T00:00:00Z")
};

insertProductSafe(duplicateTestProduct);
insertProductSafe({
  ...duplicateTestProduct,
  name: "Test Widget Duplicate"
});

const discountResult = db.products.updateMany(
  { category: "Electronics", stock: { $gt: 50 } },
  { $mul: { price: NumberDecimal("0.90") } }
);
print(
  "Electronics discount update - matched: " +
    discountResult.matchedCount +
    ", modified: " +
    discountResult.modifiedCount
);

function printBlock(title, description, docs) {
  print("\n============================================================");
  print(title);
  print(description);
  print("first 3 docs:");
  printjson(docs.slice(0, 3));
}

function runQuery(title, description, cursor) {
  const docs = cursor.toArray();
  printBlock(title, description, docs);
}

// Queries
runQuery(
  "Q1 - Books with rating >= 4.0 and stock > 0",
  "Returns in-stock highly-rated books, projected fields only, sorted by price ascending.",
  db.products
    .find(
      {
        category: "Books",
        "ratings.average": { $gte: 4.0 },
        stock: { $gt: 0 }
      },
      {
        _id: 0,
        name: 1,
        price: 1,
        "ratings.average": 1,
        tags: 1
      }
    )
    .sort({ price: 1 })
);

runQuery(
  "Q2A - Tagged with both new-arrival AND featured",
  "Uses $all to require both tags in the same product.",
  db.products.find(
    { tags: { $all: ["new-arrival", "featured"] } },
    { _id: 0, sku: 1, name: 1, tags: 1 }
  )
);

runQuery(
  "Q2B - Tagged with clearance OR sale",
  "Uses $in to match products that contain at least one of the two tags.",
  db.products.find(
    { tags: { $in: ["clearance", "sale"] } },
    { _id: 0, sku: 1, name: 1, tags: 1 }
  )
);

runQuery(
  "Q3 - Full-text search for \"wireless headphones\"",
  "Returns text matches ranked by textScore.",
  db.products
    .find(
      { $text: { $search: "wireless headphones" } },
      {
        _id: 0,
        score: { $meta: "textScore" },
        name: 1,
        price: 1
      }
    )
    .sort({ score: { $meta: "textScore" } })
);

runQuery(
  "Q4 - Gold customers in Greece or Germany",
  "Filters nested address.country and tier, then projects name, email, address.",
  db.customers.find(
    {
      "address.country": { $in: ["Greece", "Germany"] },
      tier: "gold"
    },
    { _id: 0, name: 1, email: 1, address: 1 }
  )
);

runQuery(
  "Q5 - Orders with an item qty > 3",
  "Uses $elemMatch on embedded items array.",
  db.orders.find(
    {
      items: {
        $elemMatch: { qty: { $gt: 3 } }
      }
    },
    { _id: 1, customer_id: 1, status: 1, items: 1, created_at: 1 }
  )
);

const dateWindowStart = ISODate("2026-03-19T00:00:00Z");
const dateWindowEnd = ISODate("2026-04-18T00:00:00Z");
runQuery(
  "Q6 - Delivered orders in the last 30 days of seed timeline",
  "Uses $gte/$lte on created_at and sorts newest first.",
  db.orders
    .find(
      {
        status: "delivered",
        created_at: { $gte: dateWindowStart, $lte: dateWindowEnd }
      },
      { _id: 1, customer_id: 1, status: 1, total: 1, created_at: 1 }
    )
    .sort({ created_at: -1 })
);

// 4. Aggregation pipelines
const revenueByCategory = db.orders
  .aggregate([
    { $match: { status: "delivered" } },
    { $unwind: "$items" },
    {
      $lookup: {
        from: "products",
        localField: "items.product_id",
        foreignField: "_id",
        as: "product"
      }
    },
    { $unwind: "$product" },
    {
      $group: {
        _id: "$product.category",
        total_revenue: {
          $sum: { $multiply: ["$items.unit_price", "$items.qty"] }
        },
        product_set: { $addToSet: "$items.product_id" }
      }
    },
    {
      $project: {
        _id: 0,
        category: "$_id",
        total_revenue: 1,
        products_sold: { $size: "$product_set" }
      }
    },
    { $sort: { total_revenue: -1 } }
  ])
  .toArray();

printBlock(
  "AGG1 - Revenue by category",
  "Delivered-order revenue and number of distinct products sold per category.",
  revenueByCategory
);

const customerLifetimeValue = db.orders
  .aggregate([
    {
      $group: {
        _id: "$customer_id",
        total_orders: { $sum: 1 },
        total_spent: {
          $sum: {
            $cond: [
              { $eq: ["$status", "delivered"] },
              "$total",
              NumberDecimal("0")
            ]
          }
        },
        avg_order_value: { $avg: "$total" }
      }
    },
    {
      $lookup: {
        from: "orders",
        let: { cid: "$_id" },
        pipeline: [
          {
            $match: {
              $expr: {
                $and: [
                  { $eq: ["$customer_id", "$$cid"] },
                  { $eq: ["$status", "delivered"] }
                ]
              }
            }
          },
          { $unwind: "$items" },
          {
            $lookup: {
              from: "products",
              localField: "items.product_id",
              foreignField: "_id",
              as: "p"
            }
          },
          { $unwind: "$p" },
          {
            $group: {
              _id: "$p.category",
              units: { $sum: "$items.qty" }
            }
          },
          { $sort: { units: -1, _id: 1 } },
          { $limit: 1 }
        ],
        as: "fav"
      }
    },
    {
      $lookup: {
        from: "customers",
        localField: "_id",
        foreignField: "_id",
        as: "customer"
      }
    },
    {
      $unwind: {
        path: "$customer",
        preserveNullAndEmptyArrays: true
      }
    },
    {
      $project: {
        _id: 0,
        customer_id: "$_id",
        customer_name: { $ifNull: ["$customer.name", null] },
        total_orders: 1,
        total_spent: 1,
        avg_order_value: 1,
        favourite_category: {
          $ifNull: [{ $arrayElemAt: ["$fav._id", 0] }, null]
        }
      }
    },
    { $sort: { total_spent: -1 } },
    { $limit: 10 }
  ])
  .toArray();

printBlock(
  "AGG2 - Customer lifetime value",
  "Top 10 customers by delivered spend with favourite delivered-order category.",
  customerLifetimeValue
);

const monthBoundaries = [
  ISODate("2026-01-01T00:00:00Z"),
  ISODate("2026-02-01T00:00:00Z"),
  ISODate("2026-03-01T00:00:00Z"),
  ISODate("2026-04-01T00:00:00Z"),
  ISODate("2026-05-01T00:00:00Z")
];

const monthlyTrend = db.orders
  .aggregate([
    {
      $bucket: {
        groupBy: "$created_at",
        boundaries: monthBoundaries,
        default: "outside_window",
        output: {
          total_revenue: { $sum: "$total" },
          number_of_orders: { $sum: 1 },
          avg_order_value: { $avg: "$total" }
        }
      }
    },
    { $match: { _id: { $ne: "outside_window" } } },
    {
      $project: {
        _id: 0,
        month: { $dateToString: { format: "%Y-%m", date: "$_id" } },
        total_revenue: 1,
        number_of_orders: 1,
        avg_order_value: 1
      }
    },
    { $sort: { month: 1 } }
  ])
  .toArray();

printBlock(
  "AGG3 - Monthly sales trend ($bucket)",
  "Per-month total revenue, number of orders, and average order value.",
  monthlyTrend
);

const vendorPerformance = db.vendors
  .aggregate([
    {
      $lookup: {
        from: "products",
        localField: "_id",
        foreignField: "vendor_id",
        as: "catalog"
      }
    },
    {
      $addFields: {
        total_products_listed: { $size: "$catalog" }
      }
    },
    {
      $lookup: {
        from: "orders",
        let: { vendorId: "$_id" },
        pipeline: [
          { $match: { status: "delivered" } },
          { $unwind: "$items" },
          {
            $lookup: {
              from: "products",
              localField: "items.product_id",
              foreignField: "_id",
              as: "product"
            }
          },
          { $unwind: "$product" },
          { $match: { $expr: { $eq: ["$product.vendor_id", "$$vendorId"] } } },
          {
            $group: {
              _id: "$items.product_id",
              product_name: { $first: "$items.name" },
              units: { $sum: "$items.qty" },
              revenue: {
                $sum: { $multiply: ["$items.unit_price", "$items.qty"] }
              }
            }
          }
        ],
        as: "sales_by_product"
      }
    },
    {
      $unwind: {
        path: "$sales_by_product",
        preserveNullAndEmptyArrays: true
      }
    },
    {
      $sort: {
        _id: 1,
        "sales_by_product.units": -1,
        "sales_by_product.product_name": 1
      }
    },
    {
      $group: {
        _id: "$_id",
        vendor_name: { $first: "$name" },
        vendor_email: { $first: "$email" },
        total_products_listed: { $first: "$total_products_listed" },
        total_units_sold: {
          $sum: { $ifNull: ["$sales_by_product.units", 0] }
        },
        gross_revenue: {
          $sum: {
            $ifNull: ["$sales_by_product.revenue", NumberDecimal("0")]
          }
        },
        top_product: { $first: "$sales_by_product.product_name" }
      }
    },
    {
      $project: {
        _id: 0,
        vendor_name: 1,
        vendor_email: 1,
        total_products_listed: 1,
        total_units_sold: 1,
        gross_revenue: 1,
        top_product: { $ifNull: ["$top_product", null] }
      }
    },
    { $sort: { gross_revenue: -1 } }
  ])
  .toArray();

printBlock(
  "AGG4 - Vendor performance report",
  "Vendor catalog size, delivered units/revenue, and best-selling product by units.",
  vendorPerformance
);

print("\nDone. Script completed successfully.");
