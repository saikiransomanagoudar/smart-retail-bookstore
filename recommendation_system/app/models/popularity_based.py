import pandas as pd

class PopularityBasedRecommender:
    def __init__(self):
        self.popular_books = None

    def fit(self, df):
        rating_count = df.groupby("Book-Title").count()["Book-Rating"].reset_index()
        rating_count.rename(columns={"Book-Rating": "NumberOfVotes"}, inplace=True)
        
        rating_average = df.groupby("Book-Title")["Book-Rating"].mean().reset_index()
        rating_average.rename(columns={"Book-Rating": "AverageRatings"}, inplace=True)
        
        popularBooks = rating_count.merge(rating_average, on="Book-Title")
        
        C = popularBooks["AverageRatings"].mean()
        m = popularBooks["NumberOfVotes"].quantile(0.90)
        
        popularBooks = popularBooks[popularBooks["NumberOfVotes"] >= 250]
        popularBooks["Popularity"] = popularBooks.apply(
            lambda x: ((x["NumberOfVotes"] * x["AverageRatings"]) + (m * C)) / (x["NumberOfVotes"] + m), 
            axis=1
        )
        popularBooks = popularBooks.sort_values(by="Popularity", ascending=False)
        
        self.popular_books = popularBooks[["Book-Title", "NumberOfVotes", "AverageRatings", "Popularity"]]

    def recommend(self, n=10):
        return self.popular_books.head(n)