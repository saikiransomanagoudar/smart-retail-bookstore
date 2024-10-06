import pandas as pd
import re

def load_and_preprocess_data(books_path, ratings_path, users_path):
    books = pd.read_csv(books_path)
    ratings = pd.read_csv(ratings_path)
    users = pd.read_csv(users_path)

    print("Books Shape:", books.shape)
    print("Ratings Shape:", ratings.shape)
    print("Users Shape:", users.shape)
    print("Any null values in Books:\n", books.isnull().sum())
    print("Any null values in Ratings:\n", ratings.isnull().sum())
    print("Any null values in Users:\n", users.isnull().sum())

    books_data = books.merge(ratings, on="ISBN")
    df = books_data.copy()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=["Image-URL-S", "Image-URL-M"], axis=1, inplace=True)
    df.drop(index=df[df["Book-Rating"] == 0].index, inplace=True)
    df["Book-Title"] = df["Book-Title"].apply(lambda x: re.sub("[\W_]+", " ", x).strip())

    return df

def get_book_isbn(df, book_title):
    return df.loc[df["Book-Title"] == book_title, "ISBN"].values[0]