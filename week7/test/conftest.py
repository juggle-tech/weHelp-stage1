"""
共用的 pytest fixture
----------------------------------
test_main.py 和 test_query.py 都會用到「記憶體 SQLite 資料庫」這個 fixture,
放在 conftest.py 裡,pytest 會自動讓同資料夾下的所有測試檔案共用它,
不用每個檔案重複寫一次。
"""

import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(name="session")
def session_fixture():
    """建立一個記憶體 SQLite 資料庫,每個測試都是全新的、互不影響"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
