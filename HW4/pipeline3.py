import csv
import sqlite3 as lite

# Connect to the SQLite database
con = lite.connect("grocery.db")
cur = con.cursor()

# Step 1: Update Null Values
cur.execute("UPDATE products SET subcat = ? WHERE subcat IS NULL", ("Unknown",))

# Step 2: Update ItemType based on Products.txt
with open("Products.txt", "r") as file:
    csv_reader = csv.DictReader(file, delimiter="|")
    for row in csv_reader:
        product_name = row["Product Name"]
        new_item_type = row["itemType"]
        cur.execute("UPDATE products SET subcat = ? WHERE prod_name = ? AND subcat IS NULL", (new_item_type, product_name))

# Step 3: Correct subcategory for specific products
cur.execute("UPDATE products SET subcat = 'Muffin' WHERE prod_name LIKE '%English Muffins%' AND subcat = 'Baked Goods Other than Bread'")

# Step 4: Assign subcategories for products with null itemType
cur.execute("UPDATE products SET subcat = 'Muffin' WHERE prod_name LIKE '%Muffins%' AND subcat IS NULL")

# Step 5: Automatically assign item types based on keywords in product names
keywords_mapping = {
    "Muffin": ["muffins", "muffin"],
    "Cupcakes": ["cupcake", "cupcakes"],
    "Sauce": ["sauce"],
    "Fruit": ["Grape, orangne"],
    "Salad dressing": ["balsamic, dressing"],
    "Frozen Food": ["cheeseburgers", "burritos", "pizza", "lasagna"],  # Example keywords for frozen food
    "Health and Hygiene": ["mouthwash", "toothpaste", "shampoo", "soap"],  # Example keywords for health and hygiene products
    # Add more keywords and corresponding item types as needed
}

for item_type, keywords in keywords_mapping.items():
    for keyword in keywords:
        cur.execute("UPDATE products SET subcat = ? WHERE prod_name LIKE ? AND subcat IS NULL AND itemType = ''", (item_type, f'%{keyword}%'))

# Step 6: Generate Updated CSV File
with open("updated_products.csv", "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["Manufacturer", "Product Name", "Size", "itemType_updated", "SKU", "BasePrice"])
    cur.execute("SELECT brandName, prod_name, size, subcat, SKU, basePrice FROM products")
    rows = cur.fetchall()
    csv_writer.writerows(rows)

# Commit changes and close the database connection
con.commit()
con.close()

print("Updated products CSV file generated successfully.")