def to_input(pathfile, to='(-3,0,0)', width=8, height=8):
    return r"""
\node[canvas is zy plane at x=0] (temp) at """ + to + """ {\includegraphics[width=""" + str(
        width) + "cm" + """,height=""" + str(height) + "cm" + """]{""" + pathfile + """}};
"""


# Conv
def to_Conv(name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    """
    Create Conv layer
    :param name: name
    :param s_filer:
    :param n_filer:
    :param offset:
    :param to:
    :param width:
    :param height:
    :param depth:
    :param caption:
    :return:
    """
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name + """,
        caption=""" + caption + r""",
        xlabel={{""" + str(n_filer) + """, }},
        zlabel=""" + str(s_filer) + """,
        fill=\ConvColor,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu(name, s_filer=256, n_filer=(64, 64), offset="(0,0,0)", to="(0,0,0)", width=(2, 2), height=40,
                    depth=40, caption=" "):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """ 
    {RightBandedBox={
        name=""" + name + """,
        caption=""" + caption + """,
        xlabel={{ """ + str(n_filer[0]) + """, """ + str(n_filer[1]) + """ }},
        zlabel=""" + str(s_filer) + """,
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height=""" + str(height) + """,
        width={ """ + str(width[0]) + """ , """ + str(width[1]) + """ },
        depth=""" + str(depth) + """
        }
    };
"""


# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """ 
    {Box={
        name=""" + name + """,
        caption=""" + caption + r""",
        fill=\PoolColor,
        opacity=""" + str(opacity) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# unpool4,
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """ 
    {Box={
        name=""" + name + r""",
        caption=""" + caption + r""",
        fill=\UnpoolColor,
        opacity=""" + str(opacity) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


def to_ConvRes(name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2,
               caption=" "):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """ 
    {RightBandedBox={
        name=""" + name + """,
        caption=""" + caption + """,
        xlabel={{ """ + str(n_filer) + """, }},
        zlabel=""" + str(s_filer) + r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity=""" + str(opacity) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax(name, s_filer=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name + """,
        caption=""" + caption + """,
        zlabel=""" + str(s_filer) + """,
        fill=\SoftmaxColor,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# SoftMax
def to_SoftMax(name, s_filer=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8,
               caption=" "):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name + """,
        caption=""" + caption + """,
        xlabel={{" ","dummy"}},
        zlabel=""" + str(s_filer) + """,
        fill=\SoftmaxColor,
        opacity=""" + str(opacity) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


def to_connection(of, to):
    return r"""
\draw [connection]  (""" + of + """-east)    -- node {\midarrow} (""" + to + """-west);
"""


def to_skip(of, to, pos=1.25):
    return r"""
\path (""" + of + """-southeast) -- (""" + of + """-northeast) coordinate[pos=""" + str(pos) + """] (""" + of + """-top) ;
\path (""" + to + """-south)  -- (""" + to + """-north)  coordinate[pos=1.25] (""" + to + """-top) ;
\draw [copyconnection]  (""" + of + """-northeast)  
-- node {\copymidarrow}(""" + of + """-top)
-- node {\copymidarrow}(""" + to + """-top)
-- node {\copymidarrow} (""" + to + """-north);
"""
