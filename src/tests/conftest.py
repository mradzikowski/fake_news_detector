import pytest

from src import create_app, db
from src.api.models import News


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def add_news():
    def _add_news(title, url, credibility):
        news = News(title=title, url=url, credibility=credibility)
        db.session.add(news)
        db.session.commit()
        return news
    return _add_news
