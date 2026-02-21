import pandas as pd

ratings = pd.read_csv("data/ml-100k/u.data", sep='\t', names=['user_id','item_id','rating','timestamp'])
movies = pd.read_csv("data/ml-100k/u.item", sep='|', encoding='latin-1', names=[
    'movie_id','title','release_date','video_release_date','IMDb_URL',
    'unknown','Action','Adventure','Animation','Children\'s','Comedy','Crime',
    'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery',
    'Romance','Sci-Fi','Thriller','War','Western'
])

print(ratings.head())
print(movies.head())

print("Number of users:", ratings['user_id'].nunique())
print("Number of movies:", ratings['item_id'].nunique())
