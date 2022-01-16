from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    """Board game."""

    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100))


def connect_to_db(app, db_uri="postgresql:///games"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""
    Game.query.delete()
    
    catan = Game(name='Catan', description='Get Resources and build settlements' )
    zelda = Game(name='Zelda', description='Follow Zelda and explore old shrines and defeat evil forces.' )
    tetris = Game(name='Tetris', description='Make the shapes connect in most efficient way' )
    codenames = Game(name='Codenames', description='Find the matching patterns in a set of tiles!' )

    db.session.add_all([catan, zelda, tetris, codenames])
    db.session.commit()


if __name__ == '__main__':
    from party import app
    # postgresql:///testdb
    connect_to_db(app)
    print("Connected to DB.")
