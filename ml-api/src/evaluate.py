"""
Evaluation script for the Neural Collaborative Filtering movie recommender.
Computes RMSE, MAE, and recommendation quality metrics.
"""
import os
import torch
from torch.utils.data import DataLoader, TensorDataset

from prepareData import load_data
from model import NCF


def load_checkpoint(model_path="./models/ncf_model.pth", device=None):
    """Load trained NCF model from checkpoint."""
    if device is None:
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
    return model, checkpoint


def evaluate(
    model_path="./models/ncf_model.pth",
    data_dir="./data/ml-100k",
    batch_size=1024,
):
    """Evaluate model on test set: RMSE, MAE."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, checkpoint = load_checkpoint(model_path, device)

    # Load test data
    (
        _,
        _,
        _,
        test_users,
        test_movies,
        test_ratings,
        _,
        _,
        _,
        _,
        _,
    ) = load_data(data_dir=data_dir)

    test_dataset = TensorDataset(test_users, test_movies, test_ratings)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model.eval()
    all_preds = []
    all_actuals = []
    with torch.no_grad():
        for users, movies, ratings in test_loader:
            users = users.to(device)
            movies = movies.to(device)
            preds = model(users, movies)
            all_preds.append(preds.cpu())
            all_actuals.append(ratings)

    preds = torch.cat(all_preds)
    actuals = torch.cat(all_actuals)

    # Denormalize (scale back to 1-5)
    preds_orig = preds * 4 + 1
    actuals_orig = actuals * 4 + 1

    # Metrics
    rmse = torch.sqrt(torch.mean((preds_orig - actuals_orig) ** 2)).item()
    mae = torch.mean(torch.abs(preds_orig - actuals_orig)).item()

    n_test = len(actuals_orig)
    print("=" * 50)
    print("Evaluation Results (test set)")
    print("=" * 50)
    print(f"Test samples: {n_test}")
    print(f"RMSE: {rmse:.4f}  (lower is better)")
    print(f"MAE:  {mae:.4f}   (lower is better)")
    print("=" * 50)
    print("RMSE = root mean squared error (rating scale 1-5)")
    print("MAE  = mean absolute error (rating scale 1-5)")
    print("=" * 50)

    return {"rmse": rmse, "mae": mae}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", default="./models/ncf_model.pth")
    parser.add_argument("--data-dir", default="./data/ml-100k")
    parser.add_argument("--batch-size", type=int, default=1024)
    args = parser.parse_args()

    evaluate(
        model_path=args.model_path,
        data_dir=args.data_dir,
        batch_size=args.batch_size,
    )
