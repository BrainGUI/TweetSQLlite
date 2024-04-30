import sqlite3 as lite
import re
import matplotlib.pyplot as plt

con = lite.connect(r'tweets.db') 
cur = con.cursor()

s = 'SELECT TWEET FROM tweets WHERE TWEET LIKE "%#%"'
cur.execute(s)

rows = cur.fetchall()

hashtags_count = {}
for row in rows:
    tweet_text = row[0]
    tweet_hashtags = re.findall(r'#\w+', tweet_text)

    for hashtag in tweet_hashtags:
        hashtags_count[hashtag] = hashtags_count.get(hashtag, 0) + 1

# Sort hashtags by the number of tweets they appear in (descending order)
sorted_hashtags = sorted(hashtags_count.items(), key=lambda x: x[1], reverse=True)

hashtags, counts = zip(*sorted_hashtags[:10])
fig = plt.figure(figsize = (10,5))

top_hashtags = ['hashtags']
used = ['counts']

plt.bar(hashtags, counts, color ='purple', width = .4)
plt.xlabel('Hashtags')
plt.ylabel('Count of Hashtags')
plt.title('Top 10 Hashtags')
plt.xticks(fontsize = 5)
plt.show()