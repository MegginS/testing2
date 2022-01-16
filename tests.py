import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):

        result = self.client.get("/")
        self.assertNotIn(b"123 Magic Unicorn Way", result.data)
        self.assertIn(b"<h2>Please RSVP</h2>", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertNotIn(b"<h2>Please RSVP</h2>", result.data)
        self.assertIn(b"123 Magic Unicorn Way", result.data)



class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess['RSVP'] = True
  
    
    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games_logged_out(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = False
  
        result = self.client.get("/games")
        self.assertIn(b"Redirect", result.data)
   

    def test_games_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True


        result = self.client.get("/games")
        self.assertIn(b"Catan", result.data)
        self.assertIn(b"Zelda", result.data)
        self.assertIn(b"Follow Zelda and explore", result.data)
        self.assertIn(b"Tetris", result.data)
        self.assertIn(b"Codenames", result.data)


    # catan = Game(name='Settlers of Catan', description='Get Resources and build settlements' )
    # zelda = Game(name='Zelda: Breath of the Wild', description='Follow Zelda and explore old shrines and defeat evil forces.' )
    # tetris = Game(name='Tetris', description='Make the shapes connect in most efficient way' )
    # codenames = Game(name='Codenames', description='Find the matching patterns in a set of tiles!' )


if __name__ == "__main__":
    unittest.main()
