import sqlite3
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from Disgest_Summerizer.app import create_app  # noqa: E402


@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_articles.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            source_name TEXT,
            image TEXT,
            url TEXT,
            publishedAt TEXT,
            content TEXT,
            summary TEXT,
            likes INTEGER,
            comments INTEGER,
            shares INTEGER,
            saved BOOLEAN,
            category TEXT
        )
        """
    )

    sample_articles = [
        (
            "article-1",
            "First headline",
            "Author One",
            "Source A",
            "https://example.com/image1.jpg",
            "https://example.com/1",
            "2025-01-01T10:00:00Z",
            "Full content for article one.",
            "Summary for article one.",
            5,
            1,
            0,
            0,
            "technology",
        ),
        (
            "article-2",
            "Second headline",
            "Author Two",
            "Source B",
            "https://example.com/image2.jpg",
            "https://example.com/2",
            "2025-01-02T11:00:00Z",
            "Full content for article two.",
            "Summary for article two.",
            2,
            3,
            1,
            1,
            "business",
        ),
        (
            "article-3",
            "Third headline",
            "Author Three",
            "Source C",
            "https://example.com/image3.jpg",
            "https://example.com/3",
            "2024-12-30T09:00:00Z",
            "Full content for article three.",
            None,
            0,
            0,
            0,
            0,
            "technology",
        ),
    ]

    conn.executemany(
        """
        INSERT INTO articles (
            id, title, author, source_name, image, url, publishedAt, content, summary,
            likes, comments, shares, saved, category
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sample_articles,
    )
    conn.commit()
    conn.close()
    return str(db_path)


@pytest.fixture
def app(temp_db):
    return create_app({"TESTING": True, "DB_PATH": temp_db})


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
