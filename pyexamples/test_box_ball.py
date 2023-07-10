
import sys
sys.path.append('../')
from pycore.tikzeng import *



# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_input( '../examples/fcn8s/cats.jpg', name="input1", to='(-3,2.5,0)', width=3, height=2 ),
    to_input( '../examples/fcn8s/cats.jpg', name="input2", width=3, height=2 ),
    to_input( '../examples/fcn8s/cats.jpg', name="input3", to='(-3,-2.5,0)', width=3, height=2 ),
    # Hidden balls to be able to create arrows from inputs to features
    to_Ball(name="input1", to='(-3,2.5,0)', opacity=0, radius=0),
    to_Ball(name="input2", to='(-3,0,0)', opacity=0, radius=0),
    to_Ball(name="input3", to='(-3,-2.5,0)', opacity=0, radius=0),
    to_Box("extraction1", offset="(0,0,0)", to="(0,2,0)", depth=4, height=2),
    to_Box("extraction2", offset="(0,0,0)", to="(0,0,0)", depth=4, height=2),
    to_Box("extraction3", offset="(0,0,0)", to="(0,-2,0)", depth=4, height=2, caption="Features"),
    to_connection("input1", "extraction1"),
    to_connection("input2", "extraction2"),
    to_connection("input3", "extraction3"),
    to_SoftMax("layer1", to="(extraction2-east)", offset="(2,0,0)", s_filer=256, depth=25, caption="Layer 1"),
    to_connection("extraction1", "layer1"),
    to_connection("extraction2", "layer1"),
    to_connection("extraction3", "layer1"),
    to_SoftMax("layer2", s_filer=128, to="(layer1-east)", offset="(2,0,0)", depth=25/2, caption="Layer 2"),
    to_connection( "layer1", "layer2"),
    to_SoftMax("layer3", s_filer=10, to="(layer2-east)", offset="(2,0,0)", depth=1, caption="Layer 3"),
    to_connection("layer2", "layer3"),
    to_Ball(name="output1", to="(layer3-east)", offset="(2,1.5,0)", radius=0.75, text="y_1"),
    to_Ball(name="output2", to="(output1-south)", offset="(0,-0.25,0)", radius=0.75, text="y_2"),
    to_Ball(name="output3", to="(output2-south)", offset="(0,-0.25,0)", radius=0.75, text="y_3"),
    to_Ball(name="output4", to="(output3-south)", offset="(0,-0.25,0)", radius=0.75, text="y_4"),
    to_Ball(name="output5", to="(output4-south)", offset="(0,-0.25,0)", radius=0.75, text="y_5"),
    to_Ball(name="output6", to="(output5-south)", offset="(0,-0.25,0)", radius=0.75, text="y_6"),
    to_Ball(name="output7", to="(output6-south)", offset="(0,-0.25,0)", radius=0.75, text="y_7"),
    to_Ball(name="output8", to="(output7-south)", offset="(0,-0.25,0)", radius=0.75, text="y_8"),
    to_Ball(name="output9", to="(output8-south)", offset="(0,-0.25,0)", radius=0.75, text="y_9"),
    to_Ball(name="output10", to="(output9-south)", offset="(0,-0.25,0)", radius=0.75, text="y_{10}", caption="Output"),
    to_connection("layer3", "output1"),
    to_connection("layer3", "output2"),
    to_connection("layer3", "output3"),
    to_connection("layer3", "output4"),
    to_connection("layer3", "output5"),
    to_connection("layer3", "output6"),
    to_connection("layer3", "output7"),
    to_connection("layer3", "output8"),
    to_connection("layer3", "output9"),
    to_connection("layer3", "output10"),
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
