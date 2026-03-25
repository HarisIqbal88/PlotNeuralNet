import sys
import os


def to_head(path):
    return r"""
\documentclass[tikz,border=0pt]{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows,3d,calc}
\begin{document}
\begin{tikzpicture}
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\SoftmaxColor{rgb:magenta,5;black,7}
\def\SumColor{rgb:blue,5;green,15}
\def\ReluColor{rgb:yellow,5;red,5;white,5}
\def\BatchNormColor{rgb:blue,2;green,1;black,0.3}
\def\EmbeddingColor{rgb:orange,5;yellow,2.5;white,5}
\def\AttentionColor{rgb:red,5;orange,2.5;white,5}
\def\CatColor{rgb:purple,5;blue,2.5;white,5}
"""


def to_cor():
    return r"""
\def\FcReluColor{rgb:blue,5;red,5;white,4}
"""


def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{scope}[every node/.append style={font=\tiny}]
"""


def to_input(image_path, offset="(0,0,0)", to="(0,0,0)", width=8, height=8, name="input"):
    return f"""
% Input
\\node[canvas is zy plane at x=0] ({name}) at {offset} {{
    \\includegraphics[width={width}cm, height={height}cm]{{{image_path}}}
}};
"""


def to_Conv(name, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40, n_filer=64, caption=" "):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption={caption},
            xlabel={{{n_filer}}},
            zlabel=,
            fill=\\ConvColor,
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_ConvRelu(name, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40, n_filer=64, caption=" "):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        RightBandedBox={{
            name={name},
            caption={caption},
            xlabel={{{n_filer}}},
            zlabel=,
            fill=\\ConvColor,
            bandfill=\\ReluColor,
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_ConvConvRelu(name, offset="(0,0,0)", to="(0,0,0)", width=(2, 2), height=40, depth=40, n_filer=(64, 64),
                    caption=" "):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption={caption},
            xlabel={{{n_filer[0]}, {n_filer[1]}}},
            zlabel=,
            fill=\\ConvReluColor,
            height={height},
            width={{{width[0]},{width[1]}}},
            depth={depth}
        }}
    }};
"""


def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption=,
            fill=\\PoolColor,
            opacity={opacity},
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_Unpool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption=,
            fill=\\UnpoolColor,
            opacity={opacity},
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_Embedding(name, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=20, depth=20, n_filer=256, caption=" "):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption={caption},
            xlabel={{{n_filer}}},
            zlabel=,
            fill=\\EmbeddingColor,
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_MLP(name, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=20, depth=20, n_filer=256, caption=" "):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption={caption},
            xlabel={{{n_filer}}},
            zlabel=,
            fill=\\FcColor,
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_Attention(name, offset="(0,0,0)", to="(0,0,0)", width=2, height=32, depth=32, n_filer=256, caption=" "):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption={caption},
            xlabel={{{n_filer}}},
            zlabel=,
            fill=\\AttentionColor,
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_Concat(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Box={{
            name={name},
            caption=Concat,
            fill=\\CatColor,
            height={height},
            width={width},
            depth={depth}
        }}
    }};
"""


def to_Sum(name, offset="(0,0,0)", to="(0,0,0)", radius=2.5, opacity=0.6):
    return f"""
\\pic[shift={{{offset}}}] at {to}
    {{
        Ball={{
            name={name},
            fill=\\SumColor,
            opacity={opacity},
            radius={radius},
            logo=$+$
        }}
    }};
"""


def to_connection(from_node, to_node):
    return f"""
\\draw [connection]  ({from_node}-east)    -- node {{\midarrow}} ({to_node}-west);
"""


def to_skip(from_node, to_node, pos=1.25):
    return f"""
\\path (from_node-east) -- (to_node-west) coordinate[pos={pos}] (mid) ;
\\draw [copyconnection]  ({from_node}-east)  -- node {{\copymidarrow}} (mid) -- node {{\copymidarrow}} (to_node-west);
"""


def to_end():
    return r"""
\end{scope}
\end{tikzpicture}
\end{document}
"""


def to_generate(arch, filename):
    with open(filename, 'w') as f:
        for line in arch:
            f.write(line)
    print(f"Generated {filename}")


def ResidualBlock(name, botton, top, s_filer, n_filer, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5, caption=""):
    return [
        to_ConvConvRelu(name=f"{name}_conv1", offset=offset, to=f"({botton}-east)", width=(size[2], size[2]),
                        height=size[0], depth=size[1], n_filer=(n_filer, n_filer), caption=caption),
        to_connection(botton, f"{name}_conv1"),
        to_ConvConvRelu(name=f"{name}_conv2", offset="(0.25,0,0)", to=f"({name}_conv1-east)", width=(size[2], size[2]),
                        height=size[0], depth=size[1], n_filer=(n_filer, n_filer)),
        to_connection(f"{name}_conv1", f"{name}_conv2"),
        to_Sum(name=f"{name}_sum", offset="(0.25,0,0)", to=f"({name}_conv2-east)", radius=size[2] / 2, opacity=opacity),
        to_connection(f"{name}_conv2", f"{name}_sum"),
        to_connection(botton, f"{name}_sum"),
        to_ConvRelu(name=f"{name}_relu", offset="(0.25,0,0)", to=f"({name}_sum-east)", width=size[2], height=size[0],
                    depth=size[1], n_filer=n_filer),
        to_connection(f"{name}_sum", f"{name}_relu"),
        to_Conv(name=top, offset="(0.25,0,0)", to=f"({name}_relu-east)", width=size[2], height=size[0], depth=size[1],
                n_filer=n_filer),
        to_connection(f"{name}_relu", top)
    ]


def Downsample(name, botton, top, offset="(0.5,0,0)", size=(32, 32, 3.5), opacity=0.5):
    return [
        to_Pool(name=name, offset=offset, to=f"({botton}-east)", width=1, height=size[0], depth=size[1],
                opacity=opacity),
        to_connection(botton, name),
        to_Conv(name=top, offset="(0.5,0,0)", to=f"({name}-east)", width=size[2], height=size[0] / 2, depth=size[1] / 2,
                n_filer=int(size[2] * 2)),
        to_connection(name, top)
    ]


def Upsample(name, botton, top, offset="(0.5,0,0)", size=(32, 32, 3.5), opacity=0.5):
    return [
        to_Unpool(name=name, offset=offset, to=f"({botton}-east)", width=1, height=size[0], depth=size[1],
                  opacity=opacity),
        to_connection(botton, name),
        to_Conv(name=top, offset="(0.5,0,0)", to=f"({name}-east)", width=size[2], height=size[0] * 2, depth=size[1] * 2,
                n_filer=int(size[2] / 2)),
        to_connection(name, top)
    ]


def EmbeddingBranch(name, offset="(0,0,0)", to="(0,0,0)", dim=256, caption=""):
    return [
        to_Embedding(name=f"{name}_emb", offset=offset, to=to, n_filer=dim, caption=f"{caption} Embedding"),
        to_MLP(name=f"{name}_mlp1", offset="(0.5,0,0)", to=f"({name}_emb-east)", n_filer=dim),
        to_connection(f"{name}_emb", f"{name}_mlp1"),
        to_MLP(name=f"{name}_mlp2", offset="(0.5,0,0)", to=f"({name}_mlp1-east)", n_filer=dim),
        to_connection(f"{name}_mlp1", f"{name}_mlp2")
    ]


def ConditionalResidualBlock(name, botton, top, s_filer, n_filer, time_emb, cond_emb, offset="(1,0,0)",
                             size=(32, 32, 3.5), opacity=0.5, caption=""):
    return [
        to_ConvConvRelu(name=f"{name}_conv1", offset=offset, to=f"({botton}-east)", width=(size[2], size[2]),
                        height=size[0], depth=size[1], n_filer=(n_filer, n_filer), caption=caption),
        to_connection(botton, f"{name}_conv1"),
        # Time embedding injection
        to_Sum(name=f"{name}_timeadd", offset="(0.25,0,0)", to=f"({name}_conv1-east)", radius=size[2] / 3,
               opacity=opacity),
        to_connection(f"{name}_conv1", f"{name}_timeadd"),
        to_connection(time_emb, f"{name}_timeadd"),
        # Condition embedding injection
        to_Sum(name=f"{name}_condadd", offset="(0.25,0,0)", to=f"({name}_timeadd-east)", radius=size[2] / 3,
               opacity=opacity),
        to_connection(f"{name}_timeadd", f"{name}_condadd"),
        to_connection(cond_emb, f"{name}_condadd"),
        # Second conv
        to_ConvConvRelu(name=f"{name}_conv2", offset="(0.25,0,0)", to=f"({name}_condadd-east)",
                        width=(size[2], size[2]), height=size[0], depth=size[1], n_filer=(n_filer, n_filer)),
        to_connection(f"{name}_condadd", f"{name}_conv2"),
        # Skip connection
        to_Sum(name=f"{name}_sum", offset="(0.25,0,0)", to=f"({name}_conv2-east)", radius=size[2] / 2, opacity=opacity),
        to_connection(f"{name}_conv2", f"{name}_sum"),
        to_connection(botton, f"{name}_sum"),
        # Final activation
        to_ConvRelu(name=f"{name}_relu", offset="(0.25,0,0)", to=f"({name}_sum-east)", width=size[2], height=size[0],
                    depth=size[1], n_filer=n_filer),
        to_connection(f"{name}_sum", f"{name}_relu"),
        to_Conv(name=top, offset="(0.25,0,0)", to=f"({name}_relu-east)", width=size[2], height=size[0], depth=size[1],
                n_filer=n_filer),
        to_connection(f"{name}_relu", top)
    ]


# Architecture definition
arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # Time embedding branch (top left)
    *EmbeddingBranch(name="time", offset="(0,5,0)", to="(0,0,0)", dim=256, caption="Time"),

    # Condition embedding branch (top right)
    *EmbeddingBranch(name="cond", offset="(10,5,0)", to="(0,0,0)", dim=256, caption="Condition"),

    # Input
    to_input('../examples/fcn8s/cats.jpg', offset="(0,0,0)", to="(0,0,0)", width=4, height=4, name="input"),

    # Initial conv
    to_Conv(name="init_conv", offset="(1,0,0)", to="(input-east)", width=2, height=32, depth=32, n_filer=64,
            caption="Init Conv"),
    to_connection("input", "init_conv"),

    # Down block 1
    *ConditionalResidualBlock(name="down1", botton="init_conv", top="down1_out", s_filer=256, n_filer=64,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(1,0,0)", size=(32, 32, 2.5),
                              caption="Down1"),
    *Downsample(name="pool1", botton="down1_out", top="pool1_out", offset="(0.5,0,0)", size=(32, 32, 2.5)),

    # Down block 2
    *ConditionalResidualBlock(name="down2", botton="pool1_out", top="down2_out", s_filer=128, n_filer=128,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(1,0,0)", size=(16, 16, 3.5),
                              caption="Down2"),
    *Downsample(name="pool2", botton="down2_out", top="pool2_out", offset="(0.5,0,0)", size=(16, 16, 3.5)),

    # Down block 3
    *ConditionalResidualBlock(name="down3", botton="pool2_out", top="down3_out", s_filer=64, n_filer=128,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(1,0,0)", size=(8, 8, 3.5),
                              caption="Down3"),
    *Downsample(name="pool3", botton="down3_out", top="pool3_out", offset="(0.5,0,0)", size=(8, 8, 3.5)),

    # Down block 4
    *ConditionalResidualBlock(name="down4", botton="pool3_out", top="down4_out", s_filer=32, n_filer=256,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(1,0,0)", size=(4, 4, 5.5),
                              caption="Down4"),

    # Middle block
    *ConditionalResidualBlock(name="mid1", botton="down4_out", top="mid1_out", s_filer=32, n_filer=256,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(1,0,0)", size=(4, 4, 5.5),
                              caption="Mid1"),
    to_Attention(name="mid_attn", offset="(0.5,0,0)", to="(mid1_out-east)", width=3, height=4, depth=4, n_filer=256,
                 caption="Attention"),
    to_connection("mid1_out", "mid_attn"),
    *ConditionalResidualBlock(name="mid2", botton="mid_attn", top="mid2_out", s_filer=32, n_filer=256,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(0.5,0,0)", size=(4, 4, 5.5),
                              caption="Mid2"),

    # Up block 1
    *Upsample(name="up1_unpool", botton="mid2_out", top="up1_unpool_out", offset="(0.5,0,0)", size=(4, 4, 5.5)),
    to_Concat(name="up1_cat", offset="(0.5,0,0)", to="(up1_unpool_out-east)", width=1, height=8, depth=8),
    to_connection("up1_unpool_out", "up1_cat"),
    to_skip(of="down3_out", to="up1_cat", pos=1.25),
    *ConditionalResidualBlock(name="up1", botton="up1_cat", top="up1_out", s_filer=64, n_filer=128,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(0.5,0,0)", size=(8, 8, 3.5),
                              caption="Up1"),

    # Up block 2
    *Upsample(name="up2_unpool", botton="up1_out", top="up2_unpool_out", offset="(0.5,0,0)", size=(8, 8, 3.5)),
    to_Concat(name="up2_cat", offset="(0.5,0,0)", to="(up2_unpool_out-east)", width=1, height=16, depth=16),
    to_connection("up2_unpool_out", "up2_cat"),
    to_skip(of="down2_out", to="up2_cat", pos=1.25),
    *ConditionalResidualBlock(name="up2", botton="up2_cat", top="up2_out", s_filer=128, n_filer=128,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(0.5,0,0)", size=(16, 16, 3.5),
                              caption="Up2"),

    # Up block 3
    *Upsample(name="up3_unpool", botton="up2_out", top="up3_unpool_out", offset="(0.5,0,0)", size=(16, 16, 3.5)),
    to_Concat(name="up3_cat", offset="(0.5,0,0)", to="(up3_unpool_out-east)", width=1, height=32, depth=32),
    to_connection("up3_unpool_out", "up3_cat"),
    to_skip(of="down1_out", to="up3_cat", pos=1.25),
    *ConditionalResidualBlock(name="up3", botton="up3_cat", top="up3_out", s_filer=256, n_filer=64,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(0.5,0,0)", size=(32, 32, 2.5),
                              caption="Up3"),

    # Up block 4
    *ConditionalResidualBlock(name="up4", botton="up3_out", top="up4_out", s_filer=256, n_filer=64,
                              time_emb="time_mlp2", cond_emb="cond_mlp2", offset="(0.5,0,0)", size=(32, 32, 2.5),
                              caption="Up4"),

    # Final layers
    to_Conv(name="final_norm", offset="(0.5,0,0)", to="(up4_out-east)", width=2, height=32, depth=32, n_filer=64,
            caption="InstanceNorm"),
    to_connection("up4_out", "final_norm"),
    to_Conv(name="final_conv", offset="(0.5,0,0)", to="(final_norm-east)", width=1, height=32, depth=32, n_filer=1,
            caption="Final Conv"),
    to_connection("final_norm", "final_conv"),

    to_end()
]


def main():
    if not os.path.exists('../examples/fcn8s'):
        os.makedirs('../examples/fcn8s', exist_ok=True)
        # Create a dummy image file
        with open('../examples/fcn8s/cats.jpg', 'w') as f:
            f.write('dummy')

    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
