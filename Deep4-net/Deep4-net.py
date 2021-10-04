import sys
sys.path.append('../')
from pycore.tikzeng import *

# defined your arch
arch = [
    
    to_head( '..' ),
    to_cor(),
    to_begin(),
    
    to_input('input',name='InputData'),

    # to_Conv("conv1", 4, 1, offset="(0,0,0)", to="(0,0,0)", height=80, depth=22, width=1 ),
    # to_Conv("conv2", 4, 4, offset="(1,0,0)", to="(conv1-east)", height=80, depth=22, width=1 ),
    to_ConvConvRelu( "conv1", s_filer=4, n_filer=(1,4), offset="(0,0,0)", to="(1,0,0)", width=(3,4), height=40, depth=40, caption="ConvBlock1"),
    #to_connection( "InputData", "conv1"),
    to_BN("bn1", offset="(0.4,0,1.5)", to="(conv1-east)",height=25, depth=20, width=2,caption="BatchNorm1" ),
    to_Pool("pool1", offset="(1.5,0,1)", to="(bn1-east)",height=40, depth=20, width=1,caption="MaxPool1" ), #2x1
    to_connection( "bn1", "pool1"),

    to_ConvConvRelu( "conv2", s_filer=8, n_filer=(4,8), offset="(2.5,0,0)", to="(pool1-east)", width=(3,4), height=40, depth=38, caption="ConvBlock2"),
    to_BN("bn2", offset="(0.4,0,1.5)", to="(conv2-east)",height=25, depth=20, width=2,caption="BatchNorm2" ),
    to_Pool("pool2", offset="(1.5,0,1)", to="(bn2-east)",height=40, depth=20, width=1,caption="MaxPool2" ), #2x1
    to_connection( "pool1", "conv2"),
    to_connection( "bn2", "pool2"),

    to_ConvConvRelu( "conv3", s_filer=16, n_filer=(8,16), offset="(2.5,0,0)", to="(pool2-east)", width=(3,4), height=40, depth=36, caption="ConvBlock3"),
    to_BN("bn3", offset="(0.4,0,1.5)", to="(conv3-east)",height=25, depth=20, width=2,caption="BatchNorm3" ),
    to_Pool("pool3", offset="(1.5,0,1)", to="(bn3-east)",height=40, depth=25, width=1,caption="MaxPool3" ), #2x2
    to_connection( "pool2", "conv3"),
    to_connection( "bn3", "pool3"),

    to_ConvConvRelu( "conv4", s_filer=32, n_filer=(16,32), offset="(2.5,0,0)", to="(pool3-east)", width=(3,4), height=37, depth=34, caption="ConvBlock4"),
    to_BN("bn4", offset="(0.4,0,1.5)", to="(conv4-east)",height=25, depth=20, width=2,caption="BatchNorm4" ),
    to_Pool("pool4", offset="(1.5,0,0.4)", to="(bn4-east)",height=40, depth=25, width=1,caption="MaxPool4" ), #2x2
    to_connection( "pool3", "conv4"),
    to_connection( "bn4", "pool4"),

    to_ConvConvRelu( "conv5", s_filer=64, n_filer=(32,64), offset="(2.5,0,0)", to="(pool4-east)", width=(3,4), height=34, depth=30, caption="ConvBlock5"),
    to_BN("bn5", offset="(0.5,0.6,1.5)", to="(conv5-east)",height=25, depth=20, width=2,caption="BatchNorm5" ),
    to_Pool("pool5", offset="(1.5,0,1)", to="(bn5-east)",height=40, depth=25, width=1,caption="MaxPool5" ), #2x2
    to_connection( "pool4", "conv5"),
    to_connection( "bn5", "pool5"),

    to_FulCon("fc1", 256, 128, offset="(8,0,3)", to="(pool5-east)", height=3, depth=30, width=3,caption='FC1'),
    to_FulCon("fc2", 512, 256, offset="(1,0,0)", to="(fc1-east)", height=3, depth=30, width=3,caption='FC2'),
    to_connection("pool5","fc1"),

    to_SoftMax( "SoftMaX", s_filer=2, offset="(3,0,0)", to="(fc2-east)", width=1.5, height=25, depth=40, opacity=0.8, caption="SoftMaX" ),
    to_connection("fc2","SoftMaX"),

    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
