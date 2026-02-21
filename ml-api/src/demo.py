"""
Demo script: Get movie recommendations for a user.
"""
import os
import torch

from prepareData import load_data
from model import NCF
from utils import predict_rating, recommend_top_movies


def load_model(model_path="./models/ncf_model.pth", data_dir="./data/ml-100k"):
    """Load model and data mappings."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    checkpoint = torch.load(model_path, map_location=device, weights_only=False)
    model = NCF(
        num_users=checkpoint["num_users"],
        num_items=checkpoint["num_movies"],
        embedding_dim=checkpoint.get("embedding_dim", 32),
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    # Load mappings and movie names
    (
        _,
        _,
        _,
        _,
        _,
        _,
        user2idx,
        movie2idx,
        idx2user,
        idx2movie,
        movie_names,
    ) = load_data(data_dir=data_dir)

    return model, user2idx, movie2idx, idx2user, idx2movie, movie_names, device


def main():
    model_path = "./models/ncf_model.pth"
    data_dir = "./data/ml-100k"

    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Run train.py first.")
        return

    model, user2idx, movie2idx, idx2user, idx2movie, movie_names, device = load_model(
        model_path, data_dir
    )

    # -------- DEMO PART 1: Rating prediction --------
    print("=" * 60)
    print("DEEP LEARNING MOVIE RECOMMENDER SYSTEM - DEMO")
    print("(Neural Collaborative Filtering on MovieLens 100K)")
    print("=" * 60)

    user_id = 196
    movie_id = 242
    movie_title = movie_names.get(movie_id, f"Movie {movie_id}")

    print("\n[1] RATING PREDICTION")
    print("-" * 60)
    print(f"Question: What rating would User {user_id} give to \"{movie_title}\"?")
    pred = predict_rating(model, user_id, movie_id, user2idx, movie2idx, device)
    if pred is not None:
        print(f"Answer: The model predicts {pred}/5 stars.")
    else:
        print(f"User {user_id} or movie {movie_id} not in dataset.")

    # -------- DEMO PART 2: Top-K recommendations --------
    print("\n[2] TOP-10 MOVIE RECOMMENDATIONS")
    print("-" * 60)
    print(f"For User {user_id}, the model suggests these 10 movies (highest predicted rating):")
    print()

    recommendations = recommend_top_movies(
        model, user_id, user2idx, movie2idx, idx2movie, movie_names, top_k=10, device=device
    )

    for i, (mid, title, pred_rating) in enumerate(recommendations, 1):
        title_show = (title[:52] + "..") if len(title) > 54 else title
        print(f"  {i:2}. {title_show:<54} -> {pred_rating}/5")

    print("\n" + "=" * 60)
    print("Demo complete. Model: NCF (GMF + MLP fusion).")
    print("=" * 60)


if __name__ == "__main__":
    main()
