import logging

import torch
import torch.nn as nn
from torch.nn import functional as F

logging.basicConfig(level=logging.DEBUG, filename=f"out_01.log")

torch.manual_seed(42)
block_size = 8 # max context length
batch_size = 32 # max parallely processed examples
n_iters = 10_000
eval_iters = 500
lr = 1e-2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
logging.debug(f"{device=}")


# Read dataset
path_in = "shakespeare.txt"
with open(path_in, 'r') as fh:
    text = fh.read().strip()


# Tokenizer
chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}
encode = lambda text: [stoi[ch] for ch in text]
decode = lambda ids: ''.join(itos[i] for i in ids)


# To tensor
data = torch.tensor(encode(text), dtype=torch.long)


# Subsets split
n = int(len(data) * 0.9)
train_data = data[:n]
val_data = data[n:]


# Batching
def get_batch(split):
    data = train_data if split == 'train' else val_data
    starts = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in starts])
    y = torch.stack([data[i+1:i+block_size+1] for i in starts])
    x, y = x.to(device), y.to(device)
    return x, y


# Estimate loss
@torch.no_grad()
def estimate_loss():
    out = {}
    m.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = m(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    m.train()
    return out


class BigramLanguageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets=None): # idx.shape == targets.shape == batch_size x block_size [4, 8]
        logits = self.token_embedding_table(idx) # tensor batch_size x block_size x vocab_size [4, 8, 65] ~ [Batch, Time, Channel]
        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)
        return logits, loss
    
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, _ = self(idx)
            logits = logits[:, -1, :] # [B,T,C] -> [B,C] for last Time step
            probs = F.softmax(logits, dim=1)
            idx_next = torch.multinomial(probs, num_samples=1) # [B,C] -> [B,1]; take 1 random C for each B
            idx = torch.cat((idx, idx_next), dim=1) # [B,T+1]
        return idx


m = BigramLanguageModel()
m = m.to(device)


# Optimizer
optimizer = torch.optim.AdamW(m.parameters(), lr=lr)


# Training loop
for i in range(n_iters):
    if i % eval_iters == 0:
        losses = estimate_loss()
        logging.debug(f"Step: {i:8}, train loss: {losses['train']:8.5f}, eval loss: {losses['val']:8.5f}")

    xb, yb = get_batch('train')
    logits, loss = m(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()


# Generate
idx = torch.zeros((1, 1), dtype=torch.long)
decoded = decode(m.generate(idx, max_new_tokens=1000)[0].tolist())
logging.info(decoded)
