import sys

from flask.cli import FlaskGroup

from src import create_app, db
from src.api.models import News

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    db.session.add(News(title="Poland is the best", url="thebestinpoland.com", credibility=2.0))
    db.session.add(News(title="Deforestation has been the most influenced by Brazil.", url="news.com", credibility=6.0))
    db.session.commit()


if __name__ == "__main__":
    cli()