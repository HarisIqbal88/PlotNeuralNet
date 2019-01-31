
import sys
sys.path.append('../')
from core.tikzeng import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_Conv( 'conv1', 572, 64, offset="(0,0,0)", to="(0,0,0)" ),
    to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)"),
    to_SoftMax( "soft1", "SOFT", 10 ,"(3,0,0)", "(pool1-east)"  ),
    to_connection( "pool1", "soft1"),    
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
