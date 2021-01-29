
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_input( '../examples/fcn8s/cats.jpg', to="(-.5,0,0)", height=1.5, width=1.5),
    to_Conv("conv1", 32, 1, offset="(0,0,0)", to="(0,0,0)", height=8, depth=8, width=2 ),
    to_ReLU("relu1", offset="(0,0,0)", to="(conv1-east)", height=8, depth=8, width=2),
    to_Conv("conv2", 32, 1, offset="(1.5,0,0)", to="(relu1-east)", height=8, depth=8, width=2 ),
    to_connection( "relu1", "conv2"),
    to_Sum("sum1", offset="(1.5,0,0)", to="(conv2-east)", radius=2.5, opacity=0.6),
    to_connection("conv2", "sum1"),
    to_skip( of='relu1', to='sum1', pos_of=2, pos_to=2.85),
    to_ReLU("relu2", offset="(1.5,0,0)", to="(sum1-east)", height=8, depth=8, width=2),
    to_connection("sum1", "relu2"),
    to_end()
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
