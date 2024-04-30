import sqlite3 as lite
import re

con = lite.connect(r'tweets.db') 
cur = con.cursor()

# Select the tweets containing hashtags
s = 'SELECT TWEET FROM tweets WHERE TWEET LIKE "%#%"'
cur.execute(s)

# Fetch all rows
rows = cur.fetchall()

# Extract and count unique hashtags for each tweet
unique_hashtags = set()
for row in rows:
    tweet_text = row[0]
    tweet_hashtags = (re.findall(r'#\w+', tweet_text))
    
    # Update the set of unique hashtags
    unique_hashtags.update(tweet_hashtags)

# Print the count of unique hashtags
print(f"Number of unique hashtags: {len(unique_hashtags)}")