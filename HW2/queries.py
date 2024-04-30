import sqlite3 as lite

con = lite.connect(r"grocery.db")
cur = con.cursor()

def total_rows(cursor, table_name, print_out=False):
    """ Returns the total number of rows in the database """
    cursor.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = cursor.fetchall()
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]


def table_col_info(cursor, table_name, print_out=False):
    """ Returns a list of tuples with column informations:
    (id, name, type, notnull, default_value, primary_key)
    """
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = cursor.fetchall()

    if print_out:
        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)
    return info
#how many rows?
#total_rows(cur,'transactions',True)

s = "SELECT COUNT(salePrice) as totalSales FROM transactions WHERE strftime('%Y-%m',dateBought) LIKE '2024-01'"
cur.execute(s)
rows = cur.fetchall()
for row in rows:
    print(row)