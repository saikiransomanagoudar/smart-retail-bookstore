from flask import Flask
from recommendation_system.app.routes.recommendations import recommendations_bp
from recommendation_system.app.services.recommendation_service import initialize_models

app = Flask(__name__)

# Register blueprints
app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')

# Initialize models
initialize_models('../data/Books.csv', '../data/ratings.csv', '../data/users.csv')

if __name__ == '__main__':
    app.run(debug=True)