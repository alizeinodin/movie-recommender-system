"""
Utility functions for the movie recommender system.
"""
import torch
import torch.nn.functional as F


def get_item_embedding(model, movie_id, movie2idx, device=None):
    """Return the item embedding for a movie (GMF + MLP averaged for similarity)."""
    if device is None:
        device = next(model.parameters()).device
    if movie_id not in movie2idx:
        return None
    idx = movie2idx[movie_id]
    m = torch.tensor([idx], dtype=torch.long, device=device)
    model.eval()
    with torch.no_grad():
        gmf = model.item_embedding_gmf(m)   # (1, emb_dim)
        mlp = model.item_embedding_mlp(m)   # (1, emb_dim)
        emb = (gmf + mlp) / 2
    return emb.squeeze(0)


def get_all_item_embeddings(model, movie2idx, device=None):
    """Precompute all item embeddings (num_items, emb_dim) for fast similar-movie lookup."""
    if device is None:
        device = next(model.parameters()).device
    indices = torch.tensor(sorted(movie2idx.values()), dtype=torch.long, device=device)
    model.eval()
    with torch.no_grad():
        gmf = model.item_embedding_gmf(indices)
        mlp = model.item_embedding_mlp(indices)
        all_emb = (gmf + mlp) / 2
    return all_emb


def similar_movies(
    model,
    movie_id,
    movie2idx,
    idx2movie,
    movie_names,
    top_k=10,
    exclude_self=True,
    device=None,
    all_embeddings=None,
):
    """
    Return top-k movies most similar to the given movie (by item embedding cosine similarity).

    Args:
        model: NCF model
        movie_id: Original movie ID
        movie2idx, idx2movie: Mappings
        movie_names: Dict movie_id -> title
        top_k: Number of similar movies
        exclude_self: If True, exclude the given movie from results
        device: torch device
        all_embeddings: Precomputed (num_items, emb_dim) tensor; if None, computed on the fly

    Returns:
        List of (movie_id, title, similarity_score) tuples
    """
    if device is None:
        device = next(model.parameters()).device
    if movie_id not in movie2idx:
        return []

    if all_embeddings is None:
        all_embeddings = get_all_item_embeddings(model, movie2idx, device)
    idx = movie2idx[movie_id]
    query_emb = all_embeddings[idx : idx + 1]  # (1, emb_dim)
    # Cosine similarity: (1, emb_dim) @ (num_items, emb_dim).T -> (1, num_items)
    sim = F.cosine_similarity(
        query_emb.unsqueeze(0),
        all_embeddings.unsqueeze(0),
        dim=2,
    ).squeeze(0)
    # Top-k (include extra if we exclude self)
    k = top_k + 1 if exclude_self else top_k
    k = min(k, sim.size(0))
    scores, indices = torch.topk(sim, k)
    results = []
    for i, (score_val, item_idx) in enumerate(zip(scores.tolist(), indices.tolist())):
        mid = idx2movie[item_idx]
        if exclude_self and mid == movie_id:
            continue
        results.append((mid, movie_names.get(mid, f"Movie {mid}"), round(score_val, 4)))
        if len(results) >= top_k:
            break
    return results


def predict_rating(model, user_id, movie_id, user2idx, movie2idx, device=None):
    """Predict rating for a user-movie pair."""
    if device is None:
        device = next(model.parameters()).device

    if user_id not in user2idx or movie_id not in movie2idx:
        return None

    u = torch.tensor([user2idx[user_id]], dtype=torch.long, device=device)
    m = torch.tensor([movie2idx[movie_id]], dtype=torch.long, device=device)

    model.eval()
    with torch.no_grad():
        pred = model(u, m)
        pred_orig = pred.item() * 4 + 1  # Denormalize from [0,1] to [1,5]
    return round(max(1.0, min(5.0, pred_orig)), 2)


def recommend_top_movies(
    model,
    user_id,
    user2idx,
    movie2idx,
    idx2movie,
    movie_names,
    top_k=10,
    exclude_rated=None,
    device=None,
):
    """
    Recommend top-k movies for a user.

    Args:
        model: Trained NCF model
        user_id: Original user ID (not index)
        user2idx, movie2idx: Mappings
        idx2movie: Reverse mapping movie_idx -> movie_id
        movie_names: Dict movie_id -> title
        top_k: Number of recommendations
        exclude_rated: Set of movie_ids the user has already rated (optional)
        device: torch device

    Returns:
        List of (movie_id, title, predicted_rating) tuples
    """
    if device is None:
        device = next(model.parameters()).device

    if user_id not in user2idx:
        return []

    exclude_rated = exclude_rated or set()
    user_idx = user2idx[user_id]
    u = torch.tensor([user_idx], dtype=torch.long, device=device)

    model.eval()
    # Build batch: sorted by movie_id for deterministic results
    sorted_items = sorted(movie2idx.items(), key=lambda x: x[0])
    movie_ids_batch = []
    indices_batch = []
    for movie_id, movie_idx in sorted_items:
        if movie_id in exclude_rated:
            continue
        movie_ids_batch.append(movie_id)
        indices_batch.append(movie_idx)

    if not movie_ids_batch:
        return []

    with torch.no_grad():
        u_batch = u.expand(len(indices_batch))
        m_batch = torch.tensor(indices_batch, dtype=torch.long, device=device)
        preds = model(u_batch, m_batch)
        pred_orig = preds * 4 + 1  # Denormalize [0,1] -> [1,5]
        pred_orig = pred_orig.cpu()

    k = min(top_k, len(movie_ids_batch))
    _, top_positions = torch.topk(pred_orig, k)

    results = []
    for pos in top_positions.tolist():
        movie_id = movie_ids_batch[pos]
        pred_rating = round(max(1.0, min(5.0, pred_orig[pos].item())), 2)
        title = movie_names.get(movie_id, f"Movie {movie_id}")
        results.append((movie_id, title, pred_rating))

    return results
