import sqlite3 as lite

con = lite.connect(r"bigGrocery.db")
cur = con.cursor()

s = "SELECT productName, size, SKU, SUM(salePrice) AS total_sales FROM transactions WHERE store = 'East ' GROUP BY sku ORDER BY total_sales DESC LIMIT 25"
cur.execute(s)
rows = cur.fetchall()
for row in rows:
    print(row)