import unittest
from app import app
from models import Recipe, User, Review, db


class RecipeTestCase(unittest.TestCase):

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

    def test_add_recipe(self):
        with app.app_context():
            response = self.app.post('/recipes/', json={'name': 'Pasta', 'ingredients': 'Noodles, Sauce',
                                                        'instructions': 'Boil noodles, add sauce',
                                                        'nutritional_info': '200 calories'})
            self.assertEqual(response.status_code, 201)

    def test_get_recipes(self):
        with app.app_context():
            recipe = Recipe(name='Pasta', ingredients='Noodles, Sauce', instructions='Boil noodles, add sauce',
                            nutritional_info='200 calories')
            db.session.add(recipe)
            db.session.commit()
            response = self.app.get('/recipes/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Pasta', response.get_data(as_text=True))

    def test_add_review(self):
        with app.app_context():
            user = User(username='testuser', preferences='vegetarian')
            db.session.add(user)
            recipe = Recipe(name='Pasta', ingredients='Noodles, Sauce', instructions='Boil noodles, add sauce',
                            nutritional_info='200 calories')
            db.session.add(recipe)
            db.session.commit()
            response = self.app.post('/recipes/1/review', json={'user_id': 1, 'rating': 5, 'comment': 'Great recipe!'})
            self.assertEqual(response.status_code, 201)

    def test_get_reviews(self):
        with app.app_context():
            user = User(username='testuser', preferences='vegetarian')
            db.session.add(user)
            recipe = Recipe(name='Pasta', ingredients='Noodles, Sauce', instructions='Boil noodles, add sauce',
                            nutritional_info='200 calories')
            db.session.add(recipe)
            db.session.commit()
            review = Review(user_id=1, recipe_id=1, rating=5, comment='Great recipe!')
            db.session.add(review)
            db.session.commit()
            response = self.app.get('/recipes/1/reviews')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Great recipe!', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
