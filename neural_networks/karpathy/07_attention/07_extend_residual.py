# What has changed:
# residual connections have been extended for what??? and then shrinked
# 
# eval loss down to 2.03
# 
# ref code: https://github.com/karpathy/ng-video-lecture/blob/master/gpt.py
 

import logging

import torch
import torch.nn as nn
from torch.nn import functional as F

logging.basicConfig(level=logging.DEBUG, filename=f"out_07.log")

torch.manual_seed(42)
block_size = 8 # max context length
batch_size = 32 # max parallely processed examples
n_iters = 10_000
eval_iters = 500
lr = 1e-3
n_embd = 32 # previously used vocab size x vocab size, now vocab_size x n_embd ---> abstraction layer

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


class Head(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size,block_size)))

    def forward(self, x):
        B,T,C = x.shape
        q = self.query(x)
        k = self.key(x)
        wei = q @ k.transpose(-2, -1) * k.shape[-1]**-0.5 # inferred head size
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) 
        wei = F.softmax(wei, dim=-1) 
        v = self.value(x)
        out = wei @ v
        return out
    

class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.projection = nn.Linear(n_embd, n_embd)

    def forward(self, x):
        x = torch.cat([h(x) for h in self.heads], dim=-1)
        x = self.projection(x) # linear projection back into the old pathway
        return x


class FeedForward(nn.Module):
    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential( # works for each token independently
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd)
        )

    def forward(self, x):
        return self.net(x)
    

class Block(nn.Module):
    def __init__(self, n_embd, n_heads):
        super().__init__()
        head_size = n_embd // n_heads
        self.sa_heads = MultiHeadAttention(num_heads=n_heads, head_size=head_size) # we want to eventually keep the same n_embed size, but meanwhile we split it into chunks, process and concatenate
        self.ffwd = FeedForward(n_embd)

    def forward(self, x):
        x = x + self.sa_heads(x) # [B,T,C], apply one head of self attention
        x = x + self.ffwd(x) # [B,T,C]
        return x


class TransformersLanguageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(
            Block(n_embd, n_heads=4),
            Block(n_embd, n_heads=4),
            Block(n_embd, n_heads=4)
        )
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None): 
        B, T = idx.shape
        tok_emb = self.token_embedding_table(idx) # [B,T,C=n_embd]
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # [T,C], broadcasted for B dim
        x = tok_emb + pos_emb # [B,T,C]
        x = self.blocks(x)
        logits = self.lm_head(x)  #  [B,T,C=vocab_size]
        
        if targets is None:
            loss = None
        else:
            B,T,C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)
        return logits, loss
    
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] # [B,T,C] -> [B,C] for last Time step
            probs = F.softmax(logits, dim=1)
            idx_next = torch.multinomial(probs, num_samples=1) # [B,C] -> [B,1]; take 1 random C for each B
            idx = torch.cat((idx, idx_next), dim=1) # [B,T+1]
        return idx


m = TransformersLanguageModel()
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
decoded = decode(m.generate(idx, max_new_tokens=10_000)[0].tolist())
logging.info(decoded)
