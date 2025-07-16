import feedparser
from datetime import datetime, timedelta, timezone
import csv
import os

def clean_text(text):
    return text.replace('"', '').replace("'", '').strip()

def fetch_tass_world(hours_cutoff=169, feed_url='https://tass.com/rss/v2.xml'):
    feed = feedparser.parse(feed_url)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_cutoff)
    results = []

    for entry in feed.entries:
        if not hasattr(entry, 'published_parsed'):
            continue
        pub = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        if pub < cutoff:
            continue
        results.append({'title': entry.title, 'link': entry.link})
    return results

def save_to_csv(items, filename='tass.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['title', 'link'],
            quoting=csv.QUOTE_ALL  # Aquí todas las celdas van entre comillas dobles
        )
        writer.writeheader()
        for item in items:
            cleaned_item = {
                'title': clean_text(item['title']),
                'link': clean_text(item['link'])
            }
            writer.writerow(cleaned_item)
    os.system("mv tass.csv current")

items = fetch_tass_world()
save_to_csv(items)
print(f"Saved {len(items)} 'tass.csv'")
