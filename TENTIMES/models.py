from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Define the base class for the database models
Base = declarative_base()

# Define the NewsArticle model (table)
class NewsArticle(Base):
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    publication_date = Column(DateTime, nullable=False)
    source_url = Column(String(255), nullable=False, unique=True)
    category = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Set up the database connection
DATABASE_URL = "postgresql://postgres:Hipanda@localhost/news_db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Create the tables in the database

# Create a session to interact with the database
SessionLocal = sessionmaker(bind=engine)