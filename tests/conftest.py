from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from bot import database


@pytest.fixture(autouse=True)
def isolated_database(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    database.Base.metadata.create_all(bind=engine)
    monkeypatch.setattr(database, "SessionLocal", sessionmaker(bind=engine))
    yield
    engine.dispose()


@pytest.fixture
def make_update():
    def _make(user_id=1):
        update = MagicMock()
        update.effective_user.id = user_id
        update.message.reply_text = AsyncMock()
        return update

    return _make


@pytest.fixture
def make_context():
    def _make(*args):
        return SimpleNamespace(args=list(args))

    return _make


@pytest.fixture
def reply_text():
    def _text(update):
        return update.message.reply_text.call_args.args[0]

    return _text
