
import os

def to_head( projectpath ):
    pathlayers = os.path.join( projectpath, 'layers/' ).replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image 
"""

def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}   
\def\SumColor{rgb:blue,5;green,15}
"""

def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""

# layers definition

def to_input( pathfile, to='(-3,0,0)', width=8, height=8, name="temp" ):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

# Conv
def to_Conv( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu( name, s_filer=256, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer[0]) +""", """+ str(n_filer[1]) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""



# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+name+""",
        caption="""+ caption +r""",
        fill=\PoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# unpool4, 
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+ name +r""",
        caption="""+ caption +r""",
        fill=\UnpoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""



def to_ConvRes( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filer) + """, }},
        zlabel="""+ str(s_filer) +r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax( name, s_filer=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# SoftMax
def to_SoftMax( name, s_filer=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        xlabel={{" ","dummy"}},
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_Sum( name, offset="(0,0,0)", to="(0,0,0)", radius=2.5, opacity=0.6):
    return r"""
\def\logo{{"+"}},
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Ball={
        name=""" + name +""",
        caption=,
        fill=\SumColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(0*radius) +""",
        width="""+ str(0*radius) +""",
        depth="""+ str(0*radius) +""" ,
        nx="""+str(1)+""",
        ny="""+str(1)+""",
        nz="""+str(1)+""",
        radius="""+ str(radius) +""",
        }
    };
"""

# Fully connected, 
def to_Fc( name, nx=2, ny=2, nz=2, offset="(0,0,0)", to="(0,0,0)", radius=2.5, width=10, height=10, depth=10, caption=" ", opacity=0.6, numLogoX=-1, numLogoY=-1, numLogoZ=-1, logo=None, pad="...", withBalls=True, withBox=True, withConnections=True, color="\FcColor", cColor="black" ):
    if numLogoX < 0:
        numLogoX = nx
    if numLogoY < 0:
        numLogoY = ny
    if numLogoZ < 0:
        numLogoZ = nz
    if logo == None:
        logo = [ (z-1)*nx*ny + x*ny + y+1 for z in range(nz,0,-1) for x in range(nx) for y in range(ny) ]
    finalLogo = []
    arrows = []
    n=0
    for k in range(nz):
        for i in range(nx):
            for j in range(ny):
                if i < numLogoX and j < numLogoY and k >= nz-numLogoZ:
                    finalLogo.append(logo[n])
                    n+=1
                    if n>=len(logo):
                        n=0
                else:
                    finalLogo.append(pad)


                    
    ret = r""
    if withBalls:
        ret += r"""
\def\logo{{"""+",".join([ '"{}"'.format(x) for x in finalLogo ])+"""}},
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Ball={
        name=""" + name +""",
        caption="""+ caption +r""",
        fill="""+color+""", 
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +""" ,
        nx="""+str(nx)+""",
        ny="""+str(ny)+""",
        nz="""+str(nz)+""",
        radius="""+ str(radius) +""",
       }
    };
"""
    if withBox:
        ret +=  r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel="""+ str(nx) +""",
        ylabel="""+ str(ny) +""",
        zlabel="""+ str(nz) +""",
        fill="""+color+""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""
    if withConnections and withBalls: # need nodes to draw arrows
        for i in range(2,numLogoX+1):
            for jof in range(1,numLogoY+1):
                for kof in range(nz,nz-numLogoZ,-1):
                    for jto in range(1,numLogoY+1):
                        for kto in range(nz,nz-numLogoZ,-1):
                            arrows.append(
                                "\draw [connection, draw={color}]  ({name}+{x1}+{y1}+{z1}-east)    "
                                "-- node {{\midarrow}} ({name}+{x2}+{y2}+{z2}-west);".format(color=cColor,
                                                                                             name=name,
                                                                                             x1=i-1, y1=jof, z1=kof,
                                                                                             x2=i, y2=jto, z2=kto))

        ret += "\n".join(arrows)
        
    return ret


def to_connection( of, to, color="black"):
    return r"""
\draw [connection, draw="""+color+"""]  ("""+of+"""-east)    -- node {\midarrow} ("""+to+"""-west);
"""

def to_FullConnections( of, to, ofX=1, ofY=1, ofZ=1, toX=1, toY=1, toZ=1, color="black"):
    arrows = []
    for y1 in range(1,ofY+1):
        for z1 in range(1,ofZ+1):
            for y2 in range(1,toY+1):
                for z2 in range(1,toZ+1):
                    arrows.append(
                        "\draw [connection, draw={color}]  ({of}+{x1}+{y1}+{z1}-east)    "
                        "-- node {{\midarrow}} ({to}+{x2}+{y2}+{z2}-west);".format(color=color,
                                                                                    of=of,
                                                                                    to=to,
                                                                                    x1=toX, y1=y1, z1=z1,
                                                                                    x2=1, y2=y2, z2=z2)
                    )
    return "\n".join(arrows)

def to_skip( of, to, pos=1.25):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
\draw [copyconnection]  ("""+of+"""-northeast)  
-- node {\copymidarrow}("""+of+"""-top)
-- node {\copymidarrow}("""+to+"""-top)
-- node {\copymidarrow} ("""+to+"""-north);
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_generate( arch, pathname="file.tex" ):
    with open(pathname, "w") as f: 
        for c in arch:
            print(c)
            f.write( c )
     


