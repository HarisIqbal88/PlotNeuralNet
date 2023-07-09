import sys

sys.path.append("../")

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


def main():
    mlp = MLP()
    parser = TorchArchParser(torch_module=mlp, input_size=(1, 2))
    arch = parser.get_arch()
    to_generate(arch, pathname="./test_torch_mlp.tex")


if __name__ == "__main__":
    main()
