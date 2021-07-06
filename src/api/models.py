from sqlalchemy.sql import func

from src import db


class News(db.Model):

    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    broadcaster = db.Column(db.String(128), nullable=True)
    url = db.Column(db.String(128), nullable=True)
    date_added = db.Column(db.DateTime, default=func.now())
    credibility = db.Column(db.Float, default=0, nullable=False)

    def __init__(self, title, credibility):
        self.title = title
        self.credibility = credibility