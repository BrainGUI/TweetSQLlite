import csv
from decimal import Decimal
import random
import datetime
from datetime import date
from collections import Counter
import sqlite3 as lite
from IPython.display import clear_output

#Creates a DB if not created already
con = lite.connect(r'grocery.db') 
cur = con.cursor()

#create a customer table
cur.execute('DROP TABLE IF EXISTS customers')
cur.execute('CREATE TABLE customers(custID INT, custFname TEXT, custLname TEXT)')

#create a products table
cur.execute('DROP TABLE IF EXISTS products')
cur.execute('CREATE TABLE products(ProductKey1 INT, SKU text, prod_name TEXT, prod_classID TEXT, subcat TEXT, category TEXT, department TEXT, prod_family TEXT, size TEXT, brandName TEXT, supplier TEXT, basePrice INT)')

#create a transactions table 
cur.execute('DROP TABLE IF EXISTS transactions')
cur.execute('CREATE TABLE transactions(dateBought TEXT, custID INT, SKU TEXT, salePrice FLOAT)')

#create a start of month inventory
cur.execute('DROP TABLE IF EXISTS somInv')
cur.execute('CREATE TABLE somInv(SKU TEXT, InStock INT, NumberOrdered INT)')

#create an end of month inventory
cur.execute('DROP TABLE IF EXISTS eomInv')
cur.execute('CREATE TABLE eomInv(SKU TEXT, InStock INT, NumberOrdred INT)')

#Write values to transactions table
i = 0
with open(r"C:\Users\Bryan\Documents\DW1\SouthWest\2024_jan_southwest_purchases.csv") as csv_file:
    
    # uses header row and generates dicts
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        i = i+1
        clear_output(wait=True)
        print('Loading Row {}'.format(i))     
        
        try:
            cur.execute("INSERT INTO transactions VALUES (?,?,?,?)",(
                row['Date'],row['CustomerNumber'],row['SKU'],row['SalePrice']))
        except lite.OperationalError as err:
                print("insert error: %s", err)

#Pulls the basePrice from the products file and joins it to the conformedProducts file.
#Joins the Products table with the Conformed products table on the SKU and pulls the basePrice and adds it to the products table.             
base_prices = {}
with open(r"C:\Users\Bryan\Documents\DW1\SouthWest\Products.txt") as products_file:
    csv_reader = csv.DictReader(products_file, delimiter='|')
    for row in csv_reader:
        base_prices[row['SKU']] = row['BasePrice']

# Read values from the "conformedProducts" file and update rows with base price
with open(r"C:\Users\Bryan\Documents\DW1\SouthWest\ConformedProducts.txt") as conformed_products_file:
    csv_reader = csv.DictReader(conformed_products_file, delimiter='\t')
    for row in csv_reader:
        sku = row['sku']  
        if sku in base_prices:
            row['base_price'] = base_prices[sku]
        else:
            row['base_price'] = None 
        cur.execute("INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
            row['ProductKey1'], row['sku'], row['product_name'], row['product_class_id'], 
            row['subcategory'], row['category'], row['department'], row['product_family'], 
            row['size'], row['brandName'], row['supplier'], row['base_price']
        ))

#Write values to customers table
i = 0
with open(r"C:\Users\Bryan\Documents\DW1\SouthWest\southwest.csv") as csv_file:
    
    # uses header row and generates dicts
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        i = i+1
        clear_output(wait=True)
        print('Loading Row {}'.format(i))     
        
        try:
            cur.execute("INSERT INTO customers VALUES (?,?,?)",(
                row['cust_id'],row['first_name'],row['last_name']))
        except lite.OperationalError as err:
                print("insert error: %s", err)

#Write values to Start of Month Inventory
i = 0
with open(r"C:\Users\Bryan\Documents\DW1\SouthWest\inventory_southwest") as csv_file:
    
    # uses header row and generates dicts
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    
    for row in csv_reader:
        i = i+1
        clear_output(wait=True)
        print('Loading Row {}'.format(i))     

        # Skip the first column and start accessing from the second column onwards
        try:
            cur.execute("INSERT INTO somInv VALUES (?,?,?)", (
                row['SKU'], row['InStock'], row['NumberOrdered']))
        except lite.OperationalError as err:
            print("insert error: %s", err)

#Write values to End of Month Inventory
i = 0
with open(r"C:\Users\Bryan\Documents\DW1\SouthWest\end_month_inventory_southwest") as csv_file:
    
    # uses header row and generates dicts
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    
    for row in csv_reader:
        i = i+1
        clear_output(wait=True)
        print('Loading Row {}'.format(i))     
        
        try:
            cur.execute("INSERT INTO eomInv VALUES (?,?,?)",(
                row['SKU'], row['InStock'], row['NumberOrdered']))
        except lite.OperationalError as err:
                print("insert error: %s", err)

con.commit()