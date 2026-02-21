# How to Present This Project to Your Master

## 1. Evaluation numbers – what they mean

When you run **`python main.py evaluate`** (with venv activated), you see:

| Metric | Meaning | Good value |
|--------|---------|------------|
| **RMSE** | Root Mean Squared Error. Average “squared” prediction error, then square root. Measures how far predicted ratings are from true ratings (scale 1–5). | **Lower is better.** Typical on MovieLens 100K: ~0.90–1.0. Under 0.95 is good. |
| **MAE** | Mean Absolute Error. Average absolute difference between predicted and true ratings (scale 1–5). | **Lower is better.** Typical: ~0.70–0.80. |

**In short:**  
- **RMSE** penalizes large errors more.  
- **MAE** is the “average star error” (e.g. 0.75 ≈ predictions wrong by 0.75 stars on average).  
You can tell your master: *“We evaluate the model on a held-out test set and report RMSE and MAE on the 1–5 rating scale.”*

---

## 2. What the demo shows

When you run **`python main.py demo`**, the demo does **two things**:

1. **Rating prediction**  
   For a fixed user and movie (e.g. User 196 and one movie), the model **predicts a rating (1–5)**.  
   You can say: *“The system can predict how much a user would like a movie they haven’t rated.”*

2. **Top-10 recommendations**  
   For the same user, the model **ranks all movies** by predicted rating and shows the **top 10**.  
   You can say: *“For a given user, the system recommends the 10 movies it predicts they would rate highest.”*

So: **evaluate** = numbers (RMSE/MAE) for your report/slides; **demo** = live show of “predict rating” + “recommend movies”.

---

## 3. How to use the demo when presenting to your master

1. **Activate the environment and run the demo**
   ```bash
   cd /home/alizeinodin/Projects/recommanderSystem
   source venv/bin/activate
   python main.py demo
   ```

2. **What to say**
   - *“This is a deep learning recommender system using Neural Collaborative Filtering (NCF) on MovieLens 100K.”*
   - *“First we see a rating prediction for one user–movie pair.”*
   - *“Then we see the top 10 movies recommended for that user, with predicted ratings.”*
   - *“The model is trained on 80% of the data and evaluated with RMSE and MAE on the remaining 20%.”*

3. **Optional: show evaluation**
   ```bash
   python main.py evaluate
   ```
   Then say: *“These are our evaluation metrics: RMSE and MAE on the test set; lower is better.”*

4. **If your master asks “what is NCF?”**  
   Short answer: *“It combines matrix factorization (GMF) and a neural network (MLP) to learn user–item interactions and predict ratings.”*

---

## 4. Quick command summary

| Goal | Command (with venv activated) |
|------|-------------------------------|
| Train model | `python main.py train` |
| Show metrics (RMSE, MAE) | `python main.py evaluate` |
| Show prediction + top-10 recommendations | `python main.py demo` |

Remember: always run **`source venv/bin/activate`** in the project folder before `python main.py ...`, so that `torch` and other dependencies are available.
