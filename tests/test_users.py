import unittest
from app import app
from models import User, db


class UserTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        with app.app_context():
            response = self.app.post('/users/', json={'username': 'testuser', 'preferences': 'vegetarian'})
            self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        with app.app_context():
            user = User(username='testuser', preferences='vegetarian')
            db.session.add(user)
            db.session.commit()
            response = self.app.get('/users/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn('testuser', response.get_data(as_text=True))

    def test_update_user(self):
        with app.app_context():
            user = User(username='testuser', preferences='vegetarian')
            db.session.add(user)
            db.session.commit()
            response = self.app.put('/users/1', json={'preferences': 'vegan'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('User updated successfully!', response.get_data(as_text=True))

    def test_delete_user(self):
        with app.app_context():
            user = User(username='testuser', preferences='vegetarian')
            db.session.add(user)
            db.session.commit()
            response = self.app.delete('/users/1')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
