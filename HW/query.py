import sqlite3 as lite
con = lite.connect(r"tweets.db")

cur = con.cursor()

s = "SELECT count(TWEET) as cnt1 FROM tweets WHERE date1 BETWEEN  '2020-07-25 20:00:00' AND '2020-07-26 20:00:00' ORDER BY cnt1"
cur.execute(s)
rows = cur.fetchall()
for row in rows: 
    print(row)