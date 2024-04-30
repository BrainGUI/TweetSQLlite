import csv
import sqlite3 as lite
from IPython.display import clear_output

# Creates a DB if not created already
con = lite.connect(r'bigGrocery.db') 
cur = con.cursor()

# Create a transactions table 
cur.execute('DROP TABLE IF EXISTS transactions')
cur.execute('CREATE TABLE transactions(store TEXT, dateBought TEXT, custID INT, SKU TEXT, salePrice FLOAT)')

# File paths for purchases files for all 11 stores
store_files = {
    'Southwest': r"C:\Users\Bryan\Documents\DW1\SouthWest\2024_jan_southwest_purchases.csv",
    'SouthCentral': r"C:\Users\Bryan\Documents\DW1\SouthCentral\2024_jan_southcentral_purchases.csv",
    'SouthEast': r"C:\Users\Bryan\Documents\DW1\SouthEast\2024_jan_southeast_purchases.csv",
    'South': r"C:\Users\Bryan\Documents\DW1\South\2024_jan_south_purchases.csv",
    'Central': r"C:\Users\Bryan\Documents\DW1\Central\2024_jan_central_purchases.csv",
    'East': r"C:\Users\Bryan\Documents\DW1\East\2024_jan_east_purchases.csv",
    'West': r"C:\Users\Bryan\Documents\DW1\West\2024_jan_west_purchases.csv",
    'North': r"C:\Users\Bryan\Documents\DW1\North\2024_jan_north_purchases.csv",
    'NorthCentral': r"C:\Users\Bryan\Documents\DW1\NorthCentral\2024_jan_northcentral_purchases.csv",
    'NorthEast': r"C:\Users\Bryan\Documents\DW1\NorthEast\2024_jan_northeast_purchases.csv",
    'NorthWest': r"C:\Users\Bryan\Documents\DW1\NorthWest\2024_jan_northwest_purchases.csv"
}

# Load data from all stores into the transactions table
for store, file_path in store_files.items():
    i = 0
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            i += 1
            clear_output(wait=True)
            print(f'Loading Row {i} from {store}')
            try:
                cur.execute("INSERT INTO transactions VALUES (?,?,?,?,?)", (
                    store, row['Date'], row['CustomerNumber'], row['SKU'], row['SalePrice']))
            except lite.OperationalError as err:
                print("insert error:", err)

con.commit()

# Updates the db to include the products size and product name
# Read the Products text file and create a dictionary to map SKU to product name and size
#sku_to_product_size = {}
#with open('Products.txt', 'r') as products_file:
#    for line in products_file:
#        manufacturer, product_name, size, item_type, sku, base_price = line.strip().split('|')
#        sku_to_product_size[sku] = {'productName': product_name, 'size': size}

# Update the transactions table with product names and sizes
#cur.execute("ALTER TABLE transactions ADD COLUMN productName TEXT")
#cur.execute("ALTER TABLE transactions ADD COLUMN size TEXT")
#for sku, info in sku_to_product_size.items():
#    product_name = info['productName']
#    size = info['size']
#    cur.execute("UPDATE transactions SET productName = ?, size = ? WHERE SKU = ?", (product_name, size, sku))

# Commit the changes
#con.commit()