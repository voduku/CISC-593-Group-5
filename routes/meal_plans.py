from flask import Blueprint, request, jsonify
from models import MealPlan, db

meal_plans_bp = Blueprint('meal_plans', __name__)

@meal_plans_bp.route('/', methods=['POST'])
def create_meal_plan():
    data = request.get_json()
    user_id = data['user_id']
    plan = data['plan']
    new_meal_plan = MealPlan(user_id=user_id, plan=plan)
    db.session.add(new_meal_plan)
    db.session.commit()
    return jsonify({'message': 'Meal plan created successfully!'}), 201

@meal_plans_bp.route('/<int:user_id>', methods=['GET'])
def get_meal_plan(user_id):
    meal_plan = MealPlan.query.filter_by(user_id=user_id).first()
    if meal_plan:
        return jsonify({'meal_plan': meal_plan.plan}), 200
    else:
        return jsonify({'message': 'Meal plan not found'}), 404

@meal_plans_bp.route('/<int:user_id>', methods=['PUT'])
def update_meal_plan(user_id):
    data = request.get_json()
    meal_plan = MealPlan.query.filter_by(user_id=user_id).first()
    if meal_plan:
        meal_plan.plan = data['plan']
        db.session.commit()
        return jsonify({'message': 'Meal plan updated successfully!'}), 200
    else:
        return jsonify({'message': 'Meal plan not found'}), 404

@meal_plans_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_meal_plan(user_id):
    meal_plan = MealPlan.query.filter_by(user_id=user_id).first()
    if meal_plan:
        db.session.delete(meal_plan)
        db.session.commit()
        return jsonify({'message': 'Meal plan deleted successfully!'}), 200
    else:
        return jsonify({'message': 'Meal plan not found'}), 404
