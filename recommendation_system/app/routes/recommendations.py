from flask import Blueprint, request, jsonify
from ..services.recommendation_service import get_popularity_based_recommendations, get_content_based_recommendations

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/popular', methods=['GET'])
def popular_recommendations():
    num_recommendations = request.args.get('num_recommendations', default=10, type=int)
    recommendations = get_popularity_based_recommendations(num_recommendations)
    return jsonify({"popular-recommendations": recommendations})

@recommendations_bp.route('/content-based', methods=['GET'])
def content_based_recommendations():
    try:
        book_title = request.args.get('book_title')
        num_recommendations = request.args.get('num_recommendations', default=5, type=int)

        if not book_title:
            return jsonify({"error": "Book title is required"}), 400

        recommendations, message = get_content_based_recommendations(book_title, num_recommendations)

        if recommendations is None:
            return jsonify({"error": message}), 404

        return jsonify({
            "message": message,
            "recommendations": recommendations
        })
    except Exception as e:
        print(f"Error in content-based recommendations: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500