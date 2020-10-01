import torch
from typing import Any
import pickle
import numpy as np
import torch.distributed as torch_distrib


class LightningDistributed:

    def __init__(self, rank=None, device=None):
        self.rank = rank
        self.device = device

    def broadcast(self, x: Any):
        is_tensor = isinstance(x, torch.Tensor)
        if not is_tensor:
            x = _encode(x).to(self.device)
        torch_distrib.broadcast(x, src=self.rank)

        print('-' * 100)
        print(x)
        print(rank)
        print('-' * 100)

        if not is_tensor:
            x = _decode(x)
        return x


def _encode(obj):
    data = pickle.dumps(obj)
    data = np.frombuffer(data, dtype=np.uint8)
    return torch.from_numpy(data)


def _decode(tensor):
    data = tensor.numpy().tobytes()
    return pickle.loads(data)