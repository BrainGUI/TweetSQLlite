import sqlite3
import matplotlib.pyplot as plt

# Connect to db
conn = sqlite3.connect(r'grocery.db')
cur = conn.cursor()

#Query to get top 10 items
cur.execute("""
    SELECT transactions.SKU, SUM(transactions.salePrice * eomInv.InStock) AS total_sales,
           products.prod_name || ' (' || products.size || ')' AS item_name
    FROM transactions
    INNER JOIN eomInv ON transactions.SKU = eomInv.SKU
    INNER JOIN products ON transactions.SKU = products.SKU
    GROUP BY transactions.SKU
    ORDER BY total_sales DESC
    LIMIT 10
""")

#Fetch results
results = cur.fetchall()

#Extract SKU, total sales, and item name into separate lists
skus = [row[0] for row in results]
total_sales = [row[1] for row in results]
item_names = [row[2] for row in results]

# Create the bar chart
plt.figure(figsize=(12, 8))
plt.bar(item_names, total_sales, color='purple')
plt.xlabel('Item')
plt.ylabel('Total Sales in $')
plt.title('Top 10 Items Sold by $')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Close the connection
conn.close()