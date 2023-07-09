import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.resolve().as_posix())

from pycore import PROJECT_PATH
from pycore.tikzeng import *


# defined your arch
arch = [
    to_head(PROJECT_PATH),
    to_cor(),
    to_begin(),
    to_Conv("conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2),
    to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)"),
    to_Conv("conv2", 128, 64, offset="(1,0,0)", to="(pool1-east)", height=32, depth=32, width=2),
    to_connection("pool1", "conv2"),
    to_Pool("pool2", offset="(0,0,0)", to="(conv2-east)", height=28, depth=28, width=1),
    to_SoftMax("soft1", 10, "(3,0,0)", "(pool1-east)", caption="SOFT"),
    to_connection("pool2", "soft1"),
    to_Sum("sum1", offset="(1.5,0,0)", to="(soft1-east)", radius=2.5, opacity=0.6),
    to_connection("soft1", "sum1"),
    to_end(),
]


def test_simple():
    to_generate(arch, f"./{__name__}.tex")


if __name__ == "__main__":
    test_simple()
