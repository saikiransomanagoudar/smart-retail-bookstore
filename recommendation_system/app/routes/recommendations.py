from flask import Blueprint, request, jsonify
from ..services.recommendation_service import get_popularity_based_recommendations
from ..services.recommendation_service import get_user_based_recommendations
from ..services.recommendation_service import get_item_based_recommendations

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/popular', methods=['GET'])
def popular_recommendations():
    num_recommendations = request.args.get('num_recommendations', default=10, type=int)
    recommendations = get_popularity_based_recommendations(num_recommendations)
    return jsonify({"popular-recommendations": recommendations})

@recommendations_bp.route('/user-based', methods=['GET'])
def user_based_recommendations():
    user_id = request.args.get('user_id', type=int)
    num_recommendations = request.args.get('num_recommendations', default=10, type=int)
    recommendations = get_user_based_recommendations(user_id, num_recommendations)
    return jsonify({"user-based-recommendations": recommendations})

@recommendations_bp.route('/item-based', methods=['GET'])
def item_based_recommendations():
    user_id = request.args.get('user_id', type=int)
    num_recommendations = request.args.get('num_recommendations', default=10, type=int)
    recommendations = get_item_based_recommendations(user_id, num_recommendations)
    return jsonify({"item-based-recommendations": recommendations})
