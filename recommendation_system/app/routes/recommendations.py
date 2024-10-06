from flask import Blueprint, request, jsonify
from ..services.recommendation_service import get_popularity_based_recommendations

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/popular', methods=['GET'])
def popular_recommendations():
    num_recommendations = request.args.get('num_recommendations', default=10, type=int)
    recommendations = get_popularity_based_recommendations(num_recommendations)
    return jsonify({"popular-recommendations": recommendations})