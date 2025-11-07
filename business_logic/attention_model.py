import numpy as np


class AttentionDemo:
    """
    Self-Attention Demonstrationsmodell für Pronomen-Resolution.
    Vortrainiert auf drei Beispielsätzen.
    """

    def __init__(self):
        np.random.seed(0)

        # Trainingsdaten
        self.sentences = [
            "Anna went to the store . She bought milk .",
            "John saw a dog . He smiled .",
            "The animal didn't cross the street because it was too tired ."
        ]

        self.labels = [
            (6, 0),  # "She" -> "Anna"
            (5, 0),  # "He"  -> "John"
            (7, 1)  # "it"  -> "animal"
        ]

        # Modell initialisieren
        self._setup_model()

    def _setup_model(self):
        """Initialisiert Vokabular und Modellparameter"""
        # Tokenisierung
        self.tokenized = [s.split() for s in self.sentences]
        vocab = sorted({tok for sent in self.tokenized for tok in sent})
        self.stoi = {w: i for i, w in enumerate(vocab)}
        self.itos = {i: w for w, i in self.stoi.items()}

        # Encodierung
        self.encoded = [np.array([self.stoi[t] for t in toks], dtype=np.int64)
                        for toks in self.tokenized]

        # Modellparameter
        self.d_model = 32
        self.d_k = self.d_model
        V = len(vocab)

        self.E = (np.random.randn(V, self.d_model) / np.sqrt(self.d_model)).astype(np.float32)
        self.W_Q = (np.random.randn(self.d_model, self.d_k) / np.sqrt(self.d_model)).astype(np.float32)
        self.W_K = (np.random.randn(self.d_model, self.d_k) / np.sqrt(self.d_model)).astype(np.float32)

    def softmax(self, x, axis=-1):
        """Numerisch stabile Softmax-Funktion"""
        x = x - x.max(axis=axis, keepdims=True)
        ex = np.exp(x)
        return ex / ex.sum(axis=axis, keepdims=True)

    def attention_scores(self, X):
        """Berechnet Attention Scores"""
        Q = X @ self.W_Q
        K = X @ self.W_K
        S = (Q @ K.T) / np.sqrt(self.d_k)
        return S

    def causal_mask(self, S):
        """Wendet Causal Mask an (verhindert Zukunftsblick)"""
        n = S.shape[0]
        mask = np.triu(np.ones((n, n), dtype=bool), k=1)
        S_masked = S.copy()
        S_masked[mask] = -1e9
        return S_masked

    def sequence_forward_loss(self, tok_ids, target_pair):
        """Forward-Pass mit Loss-Berechnung"""
        X = self.E[tok_ids]
        S = self.attention_scores(X)
        S = self.causal_mask(S)
        A = self.softmax(S, axis=-1)

        p_idx, a_idx = target_pair
        loss = -np.log(max(A[p_idx, a_idx], 1e-9))
        cache = (X, S, A, p_idx, a_idx)
        return loss, cache

    def backward_update(self, tok_ids, cache, lr=0.05):
        """Backward-Pass mit Parameterupdate"""
        X, S, A, p_idx, a_idx = cache
        n = A.shape[0]

        dS = np.zeros_like(S)
        dA_row = A[p_idx].copy()
        dA_row[a_idx] -= 1.0
        dS[p_idx, :] = dA_row

        mask = np.triu(np.ones((n, n), dtype=bool), k=1)
        dS[mask] = 0.0

        Q = X @ self.W_Q
        K = X @ self.W_K
        scale = 1.0 / np.sqrt(self.d_k)

        dQ = (dS @ K) * scale
        dK = (dS.T @ Q) * scale

        dW_Q = X.T @ dQ
        dW_K = X.T @ dK
        dX = dQ @ self.W_Q.T + dK @ self.W_K.T

        self.W_Q -= lr * dW_Q.astype(np.float32)
        self.W_K -= lr * dW_K.astype(np.float32)

        for i, tok_id in enumerate(tok_ids):
            self.E[tok_id] -= (lr * dX[i]).astype(np.float32)

    def train(self, epochs=800, lr=0.05):
        """Trainiert das Modell"""
        losses = []

        for ep in range(1, epochs + 1):
            total_loss = 0.0
            for s_i in range(len(self.sentences)):
                tok_ids = self.encoded[s_i]
                target = self.labels[s_i]

                loss, cache = self.sequence_forward_loss(tok_ids, target)
                total_loss += loss
                self.backward_update(tok_ids, cache, lr)

            losses.append(total_loss)

        return losses

    def get_attention_weights(self, sentence_idx):
        """Gibt Attention-Gewichte für einen Satz zurück"""
        tok_ids = self.encoded[sentence_idx]
        X = self.E[tok_ids]
        S = self.causal_mask(self.attention_scores(X))
        A = self.softmax(S, axis=-1)

        return A

    def analyze_pronoun(self, sentence_idx):
        """Analysiert Pronomen-Attention für einen Satz"""
        A = self.get_attention_weights(sentence_idx)
        p_idx, a_idx = self.labels[sentence_idx]
        toks = self.tokenized[sentence_idx]

        row = A[p_idx]
        order = np.argsort(-row)

        top_targets = []
        for j in order[:5]:
            top_targets.append({
                'index': int(j),
                'word': toks[j],
                'weight': float(row[j]),
                'is_target': (j == a_idx)
            })

        return {
            'pronoun': toks[p_idx],
            'pronoun_idx': p_idx,
            'target': toks[a_idx],
            'target_idx': a_idx,
            'tokens': toks,
            'attention_weights': row.tolist(),
            'top_targets': top_targets
        }