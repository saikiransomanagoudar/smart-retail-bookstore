from recommendation_system.app.models.popularity_based import PopularityBasedRecommender
from recommendation_system.app.services.data_processing import load_and_preprocess_data, get_book_isbn

# Global variables
popularity_model = None
df = None

def initialize_models(books_path, ratings_path, users_path):
    global popularity_model, df
    
    df = load_and_preprocess_data(books_path, ratings_path, users_path)
    
    popularity_model = PopularityBasedRecommender()
    popularity_model.fit(df)

def get_popularity_based_recommendations(num_recommendations=10):
    if popularity_model is None:
        raise Exception("Models not initialized. Call initialize_models() first.")

    recommendations = popularity_model.recommend(num_recommendations)
    
    # Convert book titles to ISBNs
    isbn_recommendations = [get_book_isbn(df, title) for title in recommendations['Book-Title']]
    
    return isbn_recommendations