import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix

class CollaborativeFilteringRecommender:
    def __init__(self):
        self.user_similarity = None
        self.item_similarity = None
        self.df_pivot = None
        self.df = None

    def fit(self, df):
        self.df = df

        # Tuning min_book_ratings and min_user_ratings
        min_book_ratings = 50
        min_user_ratings = 10
        filtered_books = df.groupby('Book-Title').filter(lambda x: len(x) >= min_book_ratings)
        filtered_users = filtered_books.groupby('User-ID').filter(lambda x: len(x) >= min_user_ratings)
        filtered_users = filtered_users.groupby(['User-ID', 'Book-Title'], as_index=False).agg({'Book-Rating': 'mean'})
        
        self.df_pivot = filtered_users.pivot(index='User-ID', columns='Book-Title', values='Book-Rating').fillna(0)

        scaler = StandardScaler(with_mean=False)
        scaled_df = scaler.fit_transform(self.df_pivot)

        self.user_similarity = cosine_similarity(scaled_df)
        self.item_similarity = cosine_similarity(scaled_df.T)


    def recommend_user_based(self, user_id, n=10):
        if self.user_similarity is None:
            raise Exception("Model is not fitted yet.")

        try:
            user_index = self.df_pivot.index.tolist().index(user_id)
        except ValueError:
            raise Exception(f"User ID {user_id} not found in data.")

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

        try:
            user_ratings = self.df_pivot.loc[user_id]
        except KeyError:
            raise Exception(f"User ID {user_id} not found in data.")
        
        rated_books = user_ratings[user_ratings > 0].index.tolist()

        recommendations = {}
        for book in rated_books:
            try:
                book_index = self.df_pivot.columns.tolist().index(book)
            except ValueError:
                continue

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
