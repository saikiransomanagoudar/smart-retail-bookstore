import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

class CollaborativeFilteringRecommender:
    def __init__(self):
        self.user_similarity = None
        self.item_similarity = None
        self.df_pivot = None
        self.df = None

    def fit(self, df):
        self.df = df
        self.df_pivot = df.pivot_table(index='User-ID', columns='Book-Title', values='Book-Rating').fillna(0)

        scaler = StandardScaler()
        scaled_df = scaler.fit_transform(self.df_pivot)
        self.user_similarity = cosine_similarity(scaled_df)
        self.item_similarity = cosine_similarity(scaled_df.T)

    def recommend_user_based(self, user_id, n=10):
        if self.user_similarity is None:
            raise Exception("Model is not fitted yet.")

        user_index = self.df_pivot.index.tolist().index(user_id)

        user_similarities = pd.Series(self.user_similarity[user_index]).sort_values(ascending=False)
        similar_users = user_similarities.iloc[1:].index  # Exclude self

        recommendations = {}
        for similar_user in similar_users:
            similar_user_ratings = self.df_pivot.iloc[similar_user]
            unrated_books = self.df_pivot.iloc[user_index][self.df_pivot.iloc[user_index] == 0]
            rated_books_by_similar_user = similar_user_ratings[unrated_books.index]
            for book, rating in rated_books_by_similar_user.items():
                if rating > 0:
                    if book not in recommendations:
                        recommendations[book] = rating
                    else:
                        recommendations[book] += rating

        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [book for book, _ in sorted_recommendations[:n]]

    def recommend_item_based(self, user_id, n=10):
 
        if self.item_similarity is None:
            raise Exception("Model is not fitted yet.")

        user_ratings = self.df_pivot.loc[user_id]
        rated_books = user_ratings[user_ratings > 0].index.tolist()

        recommendations = {}
        for book in rated_books:
            book_index = self.df_pivot.columns.tolist().index(book)
            similar_items = pd.Series(self.item_similarity[book_index]).sort_values(ascending=False)
            similar_books = similar_items.index

            for similar_book in similar_books:
                if similar_book != book and self.df_pivot.loc[user_id, self.df_pivot.columns[similar_book]] == 0:
                    if self.df_pivot.columns[similar_book] not in recommendations:
                        recommendations[self.df_pivot.columns[similar_book]] = similar_items[similar_book]
                    else:
                        recommendations[self.df_pivot.columns[similar_book]] += similar_items[similar_book]

        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [book for book, _ in sorted_recommendations[:n]]
