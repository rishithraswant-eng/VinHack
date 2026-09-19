import math
from typing import Any

from app.core.config import settings


class HawkesEngine:
    def __init__(self, mu: float | None = None, alpha: float | None = None, beta: float | None = None):
        self.mu = mu if mu is not None else settings.HAWKES_MU
        self.alpha = alpha if alpha is not None else settings.HAWKES_ALPHA
        self.beta = beta if beta is not None else settings.HAWKES_BETA

    def _compute_intensity(self, t: float, history: list[float]) -> float:
        """
        λ(t) = μ + Σ α·e^(−β(t−tᵢ)) for all t_i < t
        """
        lambda_t = self.mu
        for t_i in history:
            if t_i < t:
                lambda_t += self.alpha * math.exp(-self.beta * (t - t_i))
        return lambda_t

    def analyze_transactions(self, transactions: list[tuple[float, float, str, str]]) -> list[dict[str, Any]]:
        """
        Input: ordered list of (timestamp, amount, from_addr, to_addr)
        Output: list of dicts with 'noise_score' and 'pruned' for each transaction.
        """
        # Ensure transactions are sorted by timestamp
        transactions = sorted(transactions, key=lambda x: x[0])
        
        results = []
        
        # Keep track of history per sender address
        history_by_sender: dict[str, list[float]] = {}
        # Keep track of peel-chain-like behavior (sender -> recipient amounts)
        amounts_by_sender: dict[str, list[float]] = {}
        
        for t, amount, from_addr, to_addr in transactions:
            if from_addr not in history_by_sender:
                history_by_sender[from_addr] = []
                amounts_by_sender[from_addr] = []
                
            sender_history = history_by_sender[from_addr]
            sender_amounts = amounts_by_sender[from_addr]
            
            # 1. Compute Hawkes intensity (noise score)
            intensity = self._compute_intensity(t, sender_history)
            
            # Normalize noise score based on some heuristics or just use intensity directly
            noise_score = intensity
            
            # 2. Heuristics for pruning
            pruned = False
            
            # Rule A: Bot-burst patterns
            # If the noise score (intensity) is very high, it means many txs happened recently.
            if noise_score > self.mu + 5 * self.alpha:  # Threshold for burst
                pruned = True
                
            # Rule B: Smurfing (micro-structuring)
            # Many small transactions from the same sender
            if len(sender_amounts) >= 3:
                recent_amounts = sender_amounts[-3:]
                # If average amount is very small and intensity is high
                if all(a < 1000 for a in recent_amounts) and noise_score > self.mu + 2 * self.alpha: # assuming 1000 sat/wei is a micro threshold
                    pruned = True
                    
            # Rule C: Peel-chains
            # A peel chain often has one large transfer and one small transfer repeatedly.
            # We look for a pattern of decreasing amounts or consecutive txs where one output is slightly smaller than the input (in UTXO, but here we just see a sequence)
            # If we see multiple txs from the same sender in short succession with large amounts
            if len(sender_amounts) >= 2:
                last_amount = sender_amounts[-1]
                # If the current amount is very similar to the last amount (minus some fee), or it's a sequence of rapid transfers
                if noise_score > self.mu + 0.5 * self.alpha and abs(amount - last_amount) / (last_amount + 1e-9) < 0.1:
                    pruned = True

            results.append({
                "noise_score": noise_score,
                "pruned": pruned
            })
            
            # Update history
            history_by_sender[from_addr].append(t)
            amounts_by_sender[from_addr].append(amount)
            
        return results
