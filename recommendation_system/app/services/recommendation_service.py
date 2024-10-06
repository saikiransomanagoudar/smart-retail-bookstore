from recommendation_system.app.models.content_based import ContentBasedRecommender
from recommendation_system.app.models.popularity_based import PopularityBasedRecommender
from recommendation_system.app.services.data_processing import load_and_preprocess_data, get_book_isbn

# Global variables
popularity_model = None
content_based_model = None
df = None

def initialize_models(books_path, ratings_path, users_path):
    global popularity_model, content_based_model, df
    
    df = load_and_preprocess_data(books_path, ratings_path, users_path)
    
    popularity_model = PopularityBasedRecommender()
    popularity_model.fit(df)

    content_based_model = ContentBasedRecommender()
    content_based_model.fit(df)

def get_popularity_based_recommendations(num_recommendations=10):
    if popularity_model is None:
        raise Exception("Models not initialized. Call initialize_models() first.")

    recommendations = popularity_model.recommend(num_recommendations)
    
    # Convert book titles to ISBNs
    isbn_recommendations = [get_book_isbn(df, title) for title in recommendations['Book-Title']]
    
    return isbn_recommendations


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