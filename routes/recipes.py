from flask import Blueprint, request, jsonify
from models import db, Recipe, Review

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['POST'])
def add_recipe():
    data = request.get_json()
    name = data['name']
    ingredients = data['ingredients']
    instructions = data['instructions']
    nutritional_info = data['nutritional_info']
    new_recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions, nutritional_info=nutritional_info)
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe added successfully!'}), 201

@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{'name': recipe.name, 'ingredients': recipe.ingredients, 'instructions': recipe.instructions, 'nutritional_info': recipe.nutritional_info} for recipe in recipes]), 200

@recipes_bp.route('/<int:recipe_id>/review', methods=['POST'])
def add_review(recipe_id):
    data = request.get_json()
    user_id = data['user_id']
    rating = data['rating']
    comment = data['comment']
    new_review = Review(user_id=user_id, recipe_id=recipe_id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added successfully!'}), 201

@recipes_bp.route('/<int:recipe_id>/reviews', methods=['GET'])
def get_reviews(recipe_id):
    reviews = Review.query.filter_by(recipe_id=recipe_id).all()
    return jsonify([{'user_id': review.user_id, 'rating': review.rating, 'comment': review.comment} for review in reviews]), 200
