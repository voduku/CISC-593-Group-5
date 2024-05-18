from flask import Flask
from routes.meal_plans import meal_plans_bp
from routes.recipes import recipes_bp
from routes.users import users_bp
from models import db

app = Flask(__name__)
app.config.from_object('config.Config')

# Registering blueprints
app.register_blueprint(meal_plans_bp, url_prefix='/meal_plans')
app.register_blueprint(recipes_bp, url_prefix='/recipes')
app.register_blueprint(users_bp, url_prefix='/users')

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
