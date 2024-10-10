import pandas as pd

def load_and_preprocess_data(books_path, ratings_path, users_path):
    books = pd.read_csv(books_path, dtype={
        'ISBN': 'str',
        'Book-Title': 'str',
        'Book-Author': 'str',
        'Year-Of-Publication': 'str',
        'Publisher': 'str',
        'Price': 'float64'
    }, low_memory=False)

    ratings = pd.read_csv(ratings_path, dtype={
        'User-ID': 'int64',
        'ISBN': 'str',
        'Book-Rating': 'int64'
    }, low_memory=False)

    users = pd.read_csv(users_path, dtype={
        'User-ID': 'int64',
        'Location': 'str',
        'Age': 'float64'
    }, low_memory=False)

    books['Year-Of-Publication'] = pd.to_numeric(books['Year-Of-Publication'], errors='coerce')

    print("Books Shape:", books.shape)
    print("Ratings Shape:", ratings.shape)
    print("Users Shape:", users.shape)

    books_data = books.merge(ratings, on="ISBN")
    df = books_data.copy()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=["Image-URL-S", "Image-URL-M"], axis=1, inplace=True)
    df.drop(index=df[df["Book-Rating"] == 0].index, inplace=True)

    return df
