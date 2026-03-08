from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 載入根目錄的 .env 檔案
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# PostgreSQL 連線字串，從環境變數讀取
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pricetracker:pricetracker123@localhost:5432/pricetracker_db"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # 自動偵測斷線並重連
    pool_size=5,           # 連線池大小
    max_overflow=10        # 超出 pool_size 時最多可額外開啟的連線數
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """提供資料庫 Session 的依賴注入函式"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
