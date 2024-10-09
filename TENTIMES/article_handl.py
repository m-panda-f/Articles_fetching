from models import SessionLocal, NewsArticle
from loguru import logger

from nlp import classify_article

def insert_article(session, article):
    existing_article = session.query(NewsArticle).filter_by(source_url=article['source_url']).first()
    if existing_article:
        logger.info(f"Duplicate article found: {article['title']}")
        return
    
    category = classify_article(article['content'])
    new_article = NewsArticle(
        title=article['title'],
        content=article['content'],
        publication_date=article['publication_date'],
        source_url=article['source_url'],
        category=category
    )
    session.add(new_article)
    session.commit()
    logger.info(f"Inserted article: {article['title']} into category: {category}")
