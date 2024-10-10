from recommendation_system.app.models.popularity_based import PopularityBasedRecommender
from recommendation_system.app.models.collaborative_filtering import CollaborativeFilteringRecommender
from recommendation_system.app.services.data_processing import load_and_preprocess_data

# Global variables
popularity_model = None
collaborative_filter_model = None
df = None

def initialize_models(books_path, ratings_path, users_path):
    global popularity_model, collaborative_filter_model, df

    df = load_and_preprocess_data(books_path, ratings_path, users_path)

    popularity_model = PopularityBasedRecommender()
    popularity_model.fit(df)

    # Initialize collaborative filtering model
    collaborative_filter_model = CollaborativeFilteringRecommender()
    collaborative_filter_model.fit(df)

def get_popularity_based_recommendations(num_recommendations=10):
    if popularity_model is None:
        raise Exception("Models not initialized. Call initialize_models() first.")

    recommendations = popularity_model.recommend(num_recommendations)
    return recommendations

def get_user_based_recommendations(user_id, num_recommendations=10):
    if collaborative_filter_model is None:
        raise Exception("Models not initialized. Call initialize_models() first.")

    return collaborative_filter_model.recommend_user_based(user_id, num_recommendations)

def get_item_based_recommendations(user_id, num_recommendations=10):
    if collaborative_filter_model is None:
        raise Exception("Models not initialized. Call initialize_models() first.")

    return collaborative_filter_model.recommend_item_based(user_id, num_recommendations)
