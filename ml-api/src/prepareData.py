"""
Data preparation module for the Deep Learning Movie Recommender System.
Loads MovieLens 100K dataset and prepares train/test splits.
"""
import os
import pandas as pd
import torch
from sklearn.model_selection import train_test_split


def load_movie_names(data_dir="./data/ml-100k"):
    """Load movie ID to title mapping from u.item file."""
    item_path = os.path.join(data_dir, "u.item")
    movie_names = {}
    with open(item_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 2:
                movie_id = int(parts[0])
                title = parts[1]
                movie_names[movie_id] = title
    return movie_names


def load_data(data_dir="./data/ml-100k", test_size=0.2, random_state=42):
    """
    Load MovieLens 100K ratings and prepare train/test splits.

    Returns:
        train_users, train_movies, train_ratings: Training data tensors
        test_users, test_movies, test_ratings: Test data tensors
        user2idx, movie2idx: Mappings from original IDs to indices
        idx2user, idx2movie: Reverse mappings for recommendation
        movie_names: Dict mapping movie_id -> title
    """
    ratings_path = os.path.join(data_dir, "u.data")
    if not os.path.exists(ratings_path):
        raise FileNotFoundError(f"Data file not found: {ratings_path}")

    ratings = pd.read_csv(
        ratings_path,
        sep="\t",
        names=["user_id", "item_id", "rating", "timestamp"],
        header=None,
    )

    # Train/test split
    train, test = train_test_split(ratings, test_size=test_size, random_state=random_state)

    # Create mappings (indices start from 0 for PyTorch Embedding)
    user_ids = ratings["user_id"].unique()
    movie_ids = ratings["item_id"].unique()
    user2idx = {uid: idx for idx, uid in enumerate(user_ids)}
    movie2idx = {mid: idx for idx, mid in enumerate(movie_ids)}
    idx2user = {idx: uid for uid, idx in user2idx.items()}
    idx2movie = {idx: mid for mid, idx in movie2idx.items()}

    # Map to indices
    train["user"] = train["user_id"].map(user2idx)
    train["movie"] = train["item_id"].map(movie2idx)
    test["user"] = test["user_id"].map(user2idx)
    test["movie"] = test["item_id"].map(movie2idx)

    # Normalize ratings to [0, 1] for neural network (original 1-5)
    train_ratings = (train["rating"].values - 1) / 4
    test_ratings = (test["rating"].values - 1) / 4

    # Convert to tensors
    train_users = torch.tensor(train["user"].values, dtype=torch.long)
    train_movies = torch.tensor(train["movie"].values, dtype=torch.long)
    train_ratings = torch.tensor(train_ratings, dtype=torch.float32)
    test_users = torch.tensor(test["user"].values, dtype=torch.long)
    test_movies = torch.tensor(test["movie"].values, dtype=torch.long)
    test_ratings = torch.tensor(test_ratings, dtype=torch.float32)

    # Load movie names for recommendation display
    movie_names = load_movie_names(data_dir)

    return (
        train_users,
        train_movies,
        train_ratings,
        test_users,
        test_movies,
        test_ratings,
        user2idx,
        movie2idx,
        idx2user,
        idx2movie,
        movie_names,
    )
