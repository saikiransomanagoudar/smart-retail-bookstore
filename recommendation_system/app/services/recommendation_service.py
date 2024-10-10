from recommendation_system.app.models.content_based import ContentBasedRecommender
from recommendation_system.app.models.popularity_based import PopularityBasedRecommender
from recommendation_system.app.models.collaborative_filtering import CollaborativeFilteringRecommender
from recommendation_system.app.services.data_processing import load_and_preprocess_data

# Global variables
popularity_model = None
collaborative_filter_model = None
content_based_model = None
df = None

def initialize_models(books_path, ratings_path, users_path):
    global popularity_model, collaborative_filter_model, content_based_model, df

    # Load and preprocess the data
    df = load_and_preprocess_data(books_path, ratings_path, users_path)

    # Initialize popularity-based model
    popularity_model = PopularityBasedRecommender()
    popularity_model.fit(df)

    # Initialize collaborative filtering model
    collaborative_filter_model = CollaborativeFilteringRecommender()
    collaborative_filter_model.fit(df)

    # Initialize content-based model
    content_based_model = ContentBasedRecommender()
    content_based_model.fit(df)

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

def get_content_based_recommendations(book_title, num_recommendations=5):
    if content_based_model is None:
        raise Exception("Models not initialized. Call initialize_models() first.")

    recommendations, status = content_based_model.recommend(book_title, num_recommendations)

    if status == "Book not found":
        return None, status
    elif status == "rare":
        return [content_based_model.get_book_details(title) for title in
                recommendations], "You may try these popular books instead:"
    else:
        return [content_based_model.get_book_details(title) for title in
                recommendations], "You may also like these books:"
