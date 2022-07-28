import torch

x=torch.rand((7))
print(x)
x=x.cumsum(0)
print(x)
ranks=torch.tensor([0,1, 1, 1,2, 2, 3], dtype=torch.int)

kept=torch.ones(x.shape[0], dtype=torch.bool)
kept[:-1] = (ranks[1:] != ranks[:-1])
print(kept )

x = x[kept]
print(x)
x = torch.cat((x[:1], x[1:] - x[:-1]))

print(x)