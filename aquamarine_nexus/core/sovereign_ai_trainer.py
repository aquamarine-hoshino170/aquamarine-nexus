import math
from typing import List, Dict, Any, Optional
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor, Linear, SGDOptimizer
from aquamarine_nexus.core.transformer_attention_engine import MultiHeadAttention, AdamWOptimizer
from aquamarine_nexus.core.lora_adapter_engine import LoRALinear

class SovereignAITrainer:
    """
    Zero-Dependency Sovereign Engine for Pre-training and LoRA Fine-Tuning.
    """

    def __init__(self, d_model: int, num_heads: int, vocab_size: int, learning_rate: float = 0.01):
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.attention = MultiHeadAttention(d_model=d_model, num_heads=num_heads)
        self.head = Linear(d_model, vocab_size)
        self.optimizer = AdamWOptimizer(self.attention.parameters() + self.head.parameters(), lr=learning_rate)

    def train_step(self, token_embeddings: List[List[float]], target_token_ids: List[int]) -> float:
        """
        Full Training Step: Computes attention, logits, cross-entropy loss, and updates all weights.
        """
        seq_len = len(token_embeddings)
        x = Tensor(token_embeddings)

        # 1. Forward Pass
        attn_out = self.attention(x)
        logits = self.head(attn_out)

        # 2. Softmax & Cross Entropy Loss
        total_loss = 0.0
        for i in range(seq_len):
            row = logits.data[i * self.vocab_size : (i + 1) * self.vocab_size]
            max_val = max(row)
            exp_vals = [math.exp(v - max_val) for v in row]
            sum_exp = sum(exp_vals)
            probs = [e / sum_exp for e in exp_vals]

            target = target_token_ids[i]
            target_prob = max(probs[target], 1e-12)
            total_loss += -math.log(target_prob)

        loss_val = total_loss / float(seq_len)
        loss_tensor = Tensor([[loss_val]])

        # 3. Backward Pass & Optimizer Step
        self.optimizer.zero_grad()
        loss_tensor.backward()
        self.optimizer.step()

        return loss_val

    def enable_lora_fine_tuning(self, rank: int = 4, alpha: float = 8.0, lr: float = 0.05):
        """
        Swaps full linear head with a frozen base and trainable LoRA low-rank matrices.
        """
        self.lora_head = LoRALinear(in_features=self.d_model, out_features=self.vocab_size, rank=rank, alpha=alpha)
        # Only LoRA parameters (A and B) will be optimized
        self.lora_optimizer = SGDOptimizer(self.lora_head.trainable_parameters(), lr=lr)

    def fine_tune_step(self, token_embeddings: List[List[float]], target_token_ids: List[int]) -> float:
        """
        Fine-Tuning Step: Updates ONLY the LoRA adapter parameters while base weights stay frozen.
        """
        if not hasattr(self, 'lora_head'):
            raise ValueError("LoRA is not enabled. Call enable_lora_fine_tuning() first.")

        seq_len = len(token_embeddings)
        x = Tensor(token_embeddings)

        # Base attention pass (frozen)
        attn_out = self.attention(x)
        # LoRA forward projection
        logits = self.lora_head(attn_out)

        # Cross Entropy Loss
        total_loss = 0.0
        for i in range(seq_len):
            row = logits.data[i * self.vocab_size : (i + 1) * self.vocab_size]
            max_val = max(row)
            exp_vals = [math.exp(v - max_val) for v in row]
            sum_exp = sum(exp_vals)
            probs = [e / sum_exp for e in exp_vals]

            target = target_token_ids[i]
            target_prob = max(probs[target], 1e-12)
            total_loss += -math.log(target_prob)

        loss_val = total_loss / float(seq_len)
        loss_tensor = Tensor([[loss_val]])

        # LoRA Optimizer backward step
        self.lora_optimizer.zero_grad()
        loss_tensor.backward()
        self.lora_optimizer.step()

        return loss_val
