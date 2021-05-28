import sys
sys.path.append('../')
from pycore.tikzeng import *

# Layer sizes

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_Fc("layer1", nx=1, ny=1, nz=1, offset="(0,0,0)", to="(0,0,0)", radius=5, opacity=0.6, width=10, height=10, depth=10, withBox=False, withConnections=False ),
    
    to_Fc("layer2", nx=1, ny=2, nz=1, offset="(3,0,0)", to="(layer1-east)", radius=2.5, opacity=0.6, width=5, height=10, depth=5,
          withBox=False, withConnections=False, logo = ["I","II"] ),
    to_FullConnections(of="layer1", to="layer2", toY=2),
    
    to_Fc("layer3", nx=1, ny=3, nz=1, offset="(3,0,0)", to="(layer2-east)", radius=2.5, opacity=0.6, width=5, height=15, depth=5,
          withBox=True, withConnections=False ),
    to_FullConnections(of="layer2", to="layer3", ofY=2, toY=3),

    to_Fc("layer4", nx=1, ny=3, nz=2, offset="(3,0,0)", to="(layer3-east)", radius=2.5, opacity=0.6, width=5, height=15, depth=10,
          withBox=True, withConnections=False ),
    to_FullConnections(of="layer3", to="layer4", ofY=3, toY=3, toZ=2),

    to_Fc("layer5", nx=2, ny=2, nz=2, offset="(3,0,0)", to="(layer4-east)", radius=2.5, opacity=0.6, width=20, height=20, depth=20,
          withBox=True, withConnections=True, cColor="green"),
    to_connection(of="layer4", to="layer5"),

    to_Fc("layer6", nx=2, ny=3, nz=2, offset="(3,0,0)", to="(layer5-east)", radius=2.5, opacity=0.6, width=15, height=22.5, depth=15,
          withBox=True, withConnections=False, logo=[1,2], numLogoY=2, numLogoX=1, numLogoZ=1, color="{rgb:blue,5;green,2.5;white,5}"),
    to_connection(of="layer5", to="layer6"),
    to_Fc("layer7", nx=2, ny=3, nz=2, offset="(3,0,0)", to="(layer6-east)", width=15, height=22.5, depth=15, withBalls=False),
    to_connection(of="layer6", to="layer7"),
    to_Sum("layer8", offset="(1.5,0,0)", to="(layer7-east)", radius=2.5, opacity=0.6),
    to_connection(of="layer7", to="layer8"),
    to_end()
    ]

def main():
    print(arch)
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()



