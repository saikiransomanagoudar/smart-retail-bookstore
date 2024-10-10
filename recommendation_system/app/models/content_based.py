import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging


class ContentBasedRecommender:
    def __init__(self):
        self.df = None
        self.common_books = None
        self.similarity = None

    def fit(self, df):
        self.df = df
        logging.info(f"DataFrame columns: {df.columns}")
        logging.info(f"DataFrame shape: {df.shape}")
        logging.info(f"DataFrame head:\n{df.head()}")

        if 'Book-Title' not in df.columns:
            raise ValueError("'Book-Title' column not found in the dataframe")

        rating_count = pd.DataFrame(df["Book-Title"].value_counts())
        rating_count = rating_count.reset_index()
        rating_count.columns = ['Book-Title', 'Count']
        rare_books = rating_count[rating_count["Count"] <= 200]["Book-Title"]
        self.common_books = df[~df["Book-Title"].isin(rare_books)]
        self.common_books = self.common_books.drop_duplicates(subset=["Book-Title"])
        self.common_books.reset_index(inplace=True, drop=True)
        self.common_books["index"] = self.common_books.index

        targets = ["Book-Title", "Book-Author", "Publisher"]
        for target in targets:
            if target not in self.common_books.columns:
                raise ValueError(f"'{target}' column not found in the dataframe")

        self.common_books["all_features"] = self.common_books[targets].apply(lambda x: " ".join(x.values.astype(str)),
                                                                             axis=1)

        vectorizer = CountVectorizer()
        common_books_vector = vectorizer.fit_transform(self.common_books["all_features"])
        self.similarity = cosine_similarity(common_books_vector)

    def recommend(self, book_title, n=5):
        if 'Book-Title' not in self.df.columns:
            return None, "DataFrame structure is incorrect"

        if book_title not in self.df["Book-Title"].values:
            return None, "Book not found"

        if book_title not in self.common_books["Book-Title"].values:
            most_common = self.common_books["Book-Title"].sample(3).values
            return most_common, "rare"

        index = self.common_books[self.common_books["Book-Title"] == book_title].index[0]
        similar_books = list(enumerate(self.similarity[index]))
        similar_books_sorted = sorted(similar_books, key=lambda x: x[1], reverse=True)[1:n + 1]

        recommended_books = [self.common_books.iloc[i[0]]["Book-Title"] for i in similar_books_sorted]
        return recommended_books, "common"

    def get_book_details(self, book_title):
        if 'Book-Title' not in self.common_books.columns:
            return None

        book_details = self.common_books[self.common_books["Book-Title"] == book_title]
        if book_details.empty:
            return None

        book_details = book_details.iloc[0]
        return {
            "title": book_details.get("Book-Title", ""),
            "author": book_details.get("Book-Author", ""),
            "publisher": book_details.get("Publisher", ""),
            "image_url": book_details.get("Image-URL-L", ""),
            "rating": round(self.df[self.df["Book-Title"] == book_title]["Book-Rating"].mean(),
                            1) if "Book-Rating" in self.df.columns else None
        }