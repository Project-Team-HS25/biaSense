# -------------------------------------------------------------
# Mini Self-Attention Proof of Concept
# Ziel: Ein Pronomen (She/He/It) soll lernen, auf sein Substantiv zu "schauen"
# -------------------------------------------------------------

import numpy as np
np.random.seed(0)  # für reproduzierbare Ergebnisse

# -------------------------------------------------------------
# 1) Mini-Datensatz
# -------------------------------------------------------------
sentences = [
    "Anna went to the store . She bought milk .",
    "John saw a dog . He smiled .",
    "The animal didn't cross the street because it was too tired ."
]

# (pronoun_index, antecedent_index)
labels = [
    (6, 0),   # "She" -> "Anna"
    (5, 0),   # "He"  -> "John"
    (7, 1)   # "it"  -> "animal"
]

# -------------------------------------------------------------
# 2) Tokenisierung & Wörterbuch
# -------------------------------------------------------------
def tokenize(text):
    return text.split()

tokenized = [tokenize(s) for s in sentences]
vocab = sorted({tok for sent in tokenized for tok in sent})
stoi = {w: i for i, w in enumerate(vocab)}   # Wort -> Index
itos = {i: w for w, i in stoi.items()}       # Index -> Wort

def encode(tokens):
    return np.array([stoi[t] for t in tokens], dtype=np.int64)

encoded = [encode(toks) for toks in tokenized]

# Debug-Ausgabe: zeigt Positionen der Tokens
for si, toks in enumerate(tokenized):
    print(f"[Satz {si}]")
    print(" ".join(f"{i}:{w}" for i, w in enumerate(toks)))

# -------------------------------------------------------------
# 3) Modellparameter
# -------------------------------------------------------------
d_model = 32   # Embedding-Dimension
d_k = d_model  # Query-/Key-Dimension
V = len(vocab) # Vokabulargröße

# Initialisierung der Parameter
E = (np.random.randn(V, d_model) / np.sqrt(d_model)).astype(np.float32)
W_Q = (np.random.randn(d_model, d_k) / np.sqrt(d_model)).astype(np.float32)
W_K = (np.random.randn(d_model, d_k) / np.sqrt(d_model)).astype(np.float32)

lr = 0.05     # Lernrate
epochs = 800  # Trainingsdurchläufe

# -------------------------------------------------------------
# 4) Hilfsfunktionen
# -------------------------------------------------------------
def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)  # für numerische Stabilität
    ex = np.exp(x)
    return ex / ex.sum(axis=axis, keepdims=True)

def attention_scores(X):
    Q = X @ W_Q
    K = X @ W_K
    S = (Q @ K.T) / np.sqrt(d_k)
    return S

def causal_mask(S):
    n = S.shape[0]
    mask = np.triu(np.ones((n, n), dtype=bool), k=1)  # Zukunft blockieren
    S_masked = S.copy()
    S_masked[mask] = -1e9
    return S_masked

# -------------------------------------------------------------
# 5) Forward-Pass + Loss
# -------------------------------------------------------------
pronouns = {"She", "He", "she", "he", "it", "It"}

def sequence_forward_loss(tok_ids, target_pair):
    X = E[tok_ids]
    S = attention_scores(X)
    S = causal_mask(S)
    A = softmax(S, axis=-1)

    p_idx, a_idx = target_pair
    loss = -np.log(max(A[p_idx, a_idx], 1e-9))  # Cross-Entropy
    cache = (X, S, A, p_idx, a_idx)
    return loss, cache

# -------------------------------------------------------------
# 6) Backward-Pass + Update
# -------------------------------------------------------------
def backward_update(tok_ids, cache):
    global E, W_Q, W_K
    X, S, A, p_idx, a_idx = cache
    n = A.shape[0]

    # Ableitung (Softmax + CrossEntropy)
    dS = np.zeros_like(S)
    dA_row = A[p_idx].copy()
    dA_row[a_idx] -= 1.0
    dS[p_idx, :] = dA_row

    # keine Gradienten für maskierte Zukunfts-Positionen
    mask = np.triu(np.ones((n, n), dtype=bool), k=1)
    dS[mask] = 0.0

    Q = X @ W_Q
    K = X @ W_K
    scale = 1.0 / np.sqrt(d_k)

    dQ = (dS @ K) * scale
    dK = (dS.T @ Q) * scale

    dW_Q = X.T @ dQ
    dW_K = X.T @ dK
    dX = dQ @ W_Q.T + dK @ W_K.T

    W_Q -= lr * dW_Q.astype(np.float32)
    W_K -= lr * dW_K.astype(np.float32)

    for i, tok_id in enumerate(tok_ids):
        E[tok_id] -= (lr * dX[i]).astype(np.float32)

# -------------------------------------------------------------
# 7) Training
# -------------------------------------------------------------
train_pairs = []
for s_i, toks in enumerate(tokenized):
    p_idx, a_idx = labels[s_i]
    if toks[p_idx] not in pronouns:
        raise ValueError(f"In Satz {s_i} ist Token {p_idx} kein Pronomen: {toks[p_idx]}")
    train_pairs.append((encoded[s_i], (p_idx, a_idx)))

for ep in range(1, epochs + 1):
    total = 0.0
    for tok_ids, target in train_pairs:
        loss, cache = sequence_forward_loss(tok_ids, target)
        total += loss
        backward_update(tok_ids, cache)
    if ep % 100 == 0:
        print(f"Epoch {ep:4d} | Loss: {total:.4f}")

# -------------------------------------------------------------
# 8) Evaluation
# -------------------------------------------------------------
def show_attention(tok_ids, toks, p_idx):
    X = E[tok_ids]
    S = causal_mask(attention_scores(X))
    A = softmax(S, axis=-1)
    row = A[p_idx]
    order = np.argsort(-row)

    print("\nSatz:", " ".join(toks))
    print(f"Pronomen @ {p_idx}: '{toks[p_idx]}'  → Top 5 Attention-Ziele:")
    for j in order[:5]:
        print(f"  - {j:2d}: {toks[j]:<10s}  w={row[j]:.3f}")

print("\n--- Evaluation ---")
for s_i, toks in enumerate(tokenized):
    tok_ids = encoded[s_i]
    p_idx, a_idx = labels[s_i]
    show_attention(tok_ids, toks, p_idx)