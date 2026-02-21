"""
Training script for the Neural Collaborative Filtering movie recommender.
Uses PyTorch DataLoader, validation split, and early stopping.
"""
import os
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from prepareData import load_data
from model import NCF


def train(
    data_dir="./data/ml-100k",
    epochs=50,
    batch_size=1024,
    lr=0.001,
    embedding_dim=32,
    patience=5,
    model_dir="./models",
):
    """Train NCF model with early stopping on validation loss."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load data
    (
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
    ) = load_data(data_dir=data_dir)

    num_users = len(user2idx)
    num_movies = len(movie2idx)
    print(f"Users: {num_users}, Movies: {num_movies}")
    print(f"Train samples: {len(train_users)}, Test samples: {len(test_users)}")

    # Create datasets and dataloaders
    train_dataset = TensorDataset(train_users, train_movies, train_ratings)
    test_dataset = TensorDataset(test_users, test_movies, test_ratings)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    # Model, loss, optimizer
    model = NCF(num_users, num_movies, embedding_dim=embedding_dim).to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    os.makedirs(model_dir, exist_ok=True)
    best_val_loss = float("inf")
    patience_counter = 0

    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0.0
        for users, movies, ratings in train_loader:
            users, movies, ratings = users.to(device), movies.to(device), ratings.to(device)
            optimizer.zero_grad()
            preds = model(users, movies)
            loss = criterion(preds, ratings)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * users.size(0)
        train_loss /= len(train_dataset)

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for users, movies, ratings in test_loader:
                users, movies, ratings = users.to(device), movies.to(device), ratings.to(device)
                preds = model(users, movies)
                loss = criterion(preds, ratings)
                val_loss += loss.item() * users.size(0)
        val_loss /= len(test_dataset)

        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            model_path = os.path.join(model_dir, "ncf_model.pth")
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "num_users": num_users,
                    "num_movies": num_movies,
                    "embedding_dim": embedding_dim,
                    "user2idx": user2idx,
                    "movie2idx": movie2idx,
                },
                model_path,
            )
            print(f"  -> Model saved (val_loss={val_loss:.4f})")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1}")
                break

    print(f"\nTraining complete. Best model saved at {model_dir}/ncf_model.pth")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="./data/ml-100k", help="Path to MovieLens data")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--embedding-dim", type=int, default=32)
    parser.add_argument("--patience", type=int, default=5)
    parser.add_argument("--model-dir", default="./models")
    args = parser.parse_args()

    train(
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        embedding_dim=args.embedding_dim,
        patience=args.patience,
        model_dir=args.model_dir,
    )
