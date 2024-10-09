import feedparser
from loguru import logger
from article_handl import insert_article
from models import SessionLocal
import schedule
import time
import csv
from datetime import datetime

# List of RSS feed URLs
RSS_FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

# Function to fetch and parse RSS feed
def fetch_rss_feed(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries:
            article = {
                'title': entry.title,
                'content': entry.description,
                'publication_date': entry.published,
                'source_url': entry.link
            }
            articles.append(article)
        return articles
    except Exception as e:
        logger.error(f"Failed to fetch or parse feed {feed_url}: {str(e)}")
        return []

# Function to fetch articles from all feeds
def fetch_all_feeds():
    all_articles = []
    for feed_url in RSS_FEEDS:
        logger.info(f"Fetching feed from {feed_url}")
        articles = fetch_rss_feed(feed_url)
        all_articles.extend(articles)
    return all_articles

# Function to write articles to a CSV file
def write_articles_to_csv(articles):
    csv_file_path = "DATA.csv"
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'content', 'publication_date', 'source_url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if the file is new
        if csv_file.tell() == 0:
            writer.writeheader()

        for article in articles:
            writer.writerow(article)

logger.add("rss_feed_log.log", rotation="1 MB")

if __name__ == "__main__":
    all_articles = fetch_all_feeds()
    logger.info(f"Fetched {len(all_articles)} articles")

    session = SessionLocal()
    for article in all_articles:
        insert_article(session, article)
    session.close()

    # Write the fetched articles to CSV after inserting into the database
    write_articles_to_csv(all_articles)

def job():
    session = SessionLocal()
    all_articles = fetch_all_feeds()
    for article in all_articles:
        insert_article(session, article)
    session.close()

    # Write the fetched articles to CSV after inserting into the database
    write_articles_to_csv(all_articles)

# Schedule the job every hour
schedule.every(1).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
