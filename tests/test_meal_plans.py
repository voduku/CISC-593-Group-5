import unittest

from app import app
from models import MealPlan, User, db

class MealPlanTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            user = User(username='testuser', preferences='vegetarian')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_meal_plan(self):
        with app.app_context():
            response = self.app.post('/meal_plans/', json={'user_id': 1, 'plan': 'test meal plan'})
            self.assertEqual(response.status_code, 201)

    def test_get_meal_plan(self):
        with app.app_context():
            meal_plan = MealPlan(user_id=1, plan='test meal plan')
            db.session.add(meal_plan)
            db.session.commit()
            response = self.app.get('/meal_plans/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn('test meal plan', response.get_data(as_text=True))

    def test_update_meal_plan(self):
        with app.app_context():
            meal_plan = MealPlan(user_id=1, plan='test meal plan')
            db.session.add(meal_plan)
            db.session.commit()
            response = self.app.put('/meal_plans/1', json={'plan': 'updated meal plan'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('Meal plan updated successfully!', response.get_data(as_text=True))

    def test_delete_meal_plan(self):
        with app.app_context():
            meal_plan = MealPlan(user_id=1, plan='test meal plan')
            db.session.add(meal_plan)
            db.session.commit()
            response = self.app.delete('/meal_plans/1')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
