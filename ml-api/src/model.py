"""
Neural Collaborative Filtering (NCF) model for movie recommendation.
Implements the GMF + MLP fusion approach from the NCF paper
(He et al., WWW 2017: Neural Collaborative Filtering).
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class NCF(nn.Module):
    """
    Neural Collaborative Filtering with GMF + MLP fusion.
    Combines Generalized Matrix Factorization and Multi-Layer Perceptron
    for learning user-item interactions.
    """

    def __init__(self, num_users, num_items, embedding_dim=32, hidden_layers=[64, 32, 16]):
        super(NCF, self).__init__()
        self.embedding_dim = embedding_dim

        # GMF embeddings (element-wise product)
        self.user_embedding_gmf = nn.Embedding(num_users, embedding_dim)
        self.item_embedding_gmf = nn.Embedding(num_items, embedding_dim)

        # MLP embeddings (concatenation)
        self.user_embedding_mlp = nn.Embedding(num_users, embedding_dim)
        self.item_embedding_mlp = nn.Embedding(num_items, embedding_dim)

        # MLP layers
        mlp_input_dim = embedding_dim * 2
        layers = []
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(mlp_input_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            mlp_input_dim = hidden_dim
        self.mlp = nn.Sequential(*layers)

        # Final prediction layer (GMF + MLP fusion)
        self.predict_layer = nn.Linear(embedding_dim + hidden_layers[-1], 1)

        self._init_weights()

    def _init_weights(self):
        nn.init.normal_(self.user_embedding_gmf.weight, std=0.01)
        nn.init.normal_(self.item_embedding_gmf.weight, std=0.01)
        nn.init.normal_(self.user_embedding_mlp.weight, std=0.01)
        nn.init.normal_(self.item_embedding_mlp.weight, std=0.01)

    def forward(self, user_ids, item_ids):
        # GMF part: element-wise product
        user_emb_gmf = self.user_embedding_gmf(user_ids)
        item_emb_gmf = self.item_embedding_gmf(item_ids)
        gmf_output = user_emb_gmf * item_emb_gmf

        # MLP part: concatenation + layers
        user_emb_mlp = self.user_embedding_mlp(user_ids)
        item_emb_mlp = self.item_embedding_mlp(item_ids)
        mlp_input = torch.cat([user_emb_mlp, item_emb_mlp], dim=-1)
        mlp_output = self.mlp(mlp_input)

        # Fusion
        fusion = torch.cat([gmf_output, mlp_output], dim=-1)
        pred = self.predict_layer(fusion)
        return pred.squeeze(-1)
