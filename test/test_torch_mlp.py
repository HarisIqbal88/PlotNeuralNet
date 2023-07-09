import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.resolve().as_posix())

import torch as th

from pycore.tikzeng import to_generate
from pycore.torchparse import TorchArchParser


class MLP(th.nn.Module):
    def __init__(self):
        super(MLP, self).__init__()

        self.net = th.nn.Sequential(
            th.nn.Linear(2, 16), th.nn.ReLU(), th.nn.Linear(16, 16), th.nn.ReLU(), th.nn.Linear(16, 1)
        )

    def forward(self, x):
        x = x.view(-1, 2)
        y_hat = self.net(x)

        return y_hat.view(-1, 1)


def test_torch_mlp():
    mlp = MLP()
    parser = TorchArchParser(torch_module=mlp, input_size=(1, 2))
    arch = parser.get_arch()
    to_generate(arch, pathname=f"./{__name__}.tex")


if __name__ == "__main__":
    test_torch_mlp()
