
import os


def _parse_offset(offset):
    if isinstance(offset, (tuple, list)):
        return tuple(float(value) for value in offset)

    cleaned = str(offset).strip()
    if cleaned.startswith("(") and cleaned.endswith(")"):
        parts = [value.strip() for value in cleaned[1:-1].split(",")]
        if len(parts) == 3:
            return tuple(float(value) for value in parts)
    raise ValueError("Offset must be a 3-tuple or '(x,y,z)' string, got {!r}".format(offset))


def _format_number(value):
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return ("{:.2f}".format(value)).rstrip("0").rstrip(".")


def _format_offset(offset):
    return "({})".format(",".join(_format_number(value) for value in offset))


def _normalize_caption(caption):
    if caption is None:
        return "{}"

    text = str(caption)
    if text.strip():
        return text
    return "{}"

def to_head( projectpath ):
    pathlayers = os.path.join( projectpath, 'layers/' ).replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{calc}
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
\def\SoftmaxColor{rgb:magenta,5;black,7}   
\def\SumColor{rgb:blue,5;green,15}
\def\PatchEmbedColor{rgb:orange,5;yellow,2;white,4}
\def\TokenColor{rgb:purple,4;blue,2;white,5}
\def\AttentionColor{rgb:cyan,5;blue,2;white,4}
\def\ReconstructColor{rgb:blue,2;green,4;white,5}
\def\ConcatColor{rgb:green,4;blue,1;white,5}
\def\QColor{rgb:blue,5;white,5}
\def\KColor{rgb:green,5;white,5}
\def\VColor{rgb:red,5;white,5}
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
\coordinate (""" + name + """-east) at (""" + name + r""".east);
\coordinate (""" + name + """-west) at (""" + name + r""".west);
"""


def to_text(name, text, to="(0,0,0)", style=r"font=\bfseries\small, align=center"):
    return (
        "\n"
        + r"\node["
        + style
        + "] ("
        + name
        + ") at "
        + to
        + " {"
        + text
        + r"};"
        + "\n"
    )

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



def to_ConvRes( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" ", fill=None, bandfill=None ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filer) + """, }},
        zlabel="""+ str(s_filer) +r""",
        fill="""+ (fill if fill is not None else '{rgb:white,1;black,3}') +""",
        bandfill="""+ (bandfill if bandfill is not None else '{rgb:white,1;black,2}') +""",
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
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Ball={
        name=""" + name +""",
        fill=\SumColor,
        opacity="""+ str(opacity) +""",
        radius="""+ str(radius) +""",
        logo=$+$
        }
    };
"""


def to_connection( of, to):
    return r"""
\draw [connection]  ("""+of+"""-east)    -- node {\midarrow} ("""+to+"""-west);
"""

def to_skip( of, to, pos=1.25):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
\draw [copyconnection]  ("""+of+"""-northeast)  
-- node {\copymidarrow}("""+of+"""-top)
-- node {\copymidarrow}("""+to+"""-top)
-- node {\copymidarrow} ("""+to+"""-north);
"""


def to_connection_anchor(of, to, src_anchor="east", dst_anchor="west", style="connection", label="\\midarrow"):
    return r"""
\draw ["""+ style +r"""]  ("""+ of +"""-"""+ src_anchor +""") -- node {"""+ label +"""} ("""+ to +"""-"""+ dst_anchor +""");
"""


def to_connection_orthogonal(of, to, src_anchor="east", dst_anchor="west", x_step=0.8, style="connection", label="\\midarrow"):
    return r"""
\draw ["""+ style +r"""] ("""+ of +"""-"""+ src_anchor +""") -- ++("""+ str(x_step) +r""",0,0) |- node {"""+ label +"""} ("""+ to +"""-"""+ dst_anchor +""");
"""


def to_skip_v2(of, to, pos=1.25, src_low="southeast", src_high="northeast", dst_low="south", dst_high="north", dst_anchor="north"):
    return r"""
\path ("""+ of +"""-"""+ src_low +""") -- ("""+ of +"""-"""+ src_high +""") coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-"""+ dst_low +""")  -- ("""+ to +"""-"""+ dst_high +""")  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
\draw [copyconnection]  ("""+of+"""-"""+ src_high +""")
-- node {\copymidarrow}("""+of+"""-top)
-- node {\copymidarrow}("""+to+"""-top)
-- node {\copymidarrow} ("""+to+"""-"""+ dst_anchor +""");
"""


def to_patch_embed(name, s_filer=16, n_filer=768, offset="(0,0,0)", to="(0,0,0)", width=2, height=12, depth=12, caption="Patch\\nEmbed"):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +"""
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\PatchEmbedColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


def to_patch_embedding(name, token_count=196, embed_dim=768, offset="(0,0,0)", to="(0,0,0)", width=(1.25, 1.25), height=12, depth=12, opacity=0.6, caption=r"Patch\\Embed"):
    caption_text = _normalize_caption(caption)
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +"""
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption_text +""",
        xlabel={{"Split", "Linear"}},
        ylabel=D="""+ str(embed_dim) +r""",
        zlabel=N="""+ str(token_count) +r""",
        fill=\PatchEmbedColor,
        bandfill=\TokenColor,
        opacity="""+ str(opacity) +""",
        bandopacity="""+ str(min(opacity + 0.12, 0.82)) +""",
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""


def to_token_block(name, s_filer=16, n_filer=768, offset="(0,0,0)", to="(0,0,0)", width=3.5, height=12, depth=12, opacity=0.55, caption="Transformer\\nEncoder"):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +"""
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer) +""", """+ str(n_filer) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\TokenColor,
        bandfill=\AttentionColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width={ """+ str(width) +""" , """+ str(width) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""


def to_transformer_encoder_stack(name, token_count=196, embed_dim=768, offset="(0,0,0)", to="(0,0,0)", width=(1.55, 1.55), height=13, depth=13, layers=12, stack=3, stack_shift=(0.36, 0.34, 0), opacity=0.62, caption="Encoder\\nLayer"):
    base_offset = _parse_offset(offset)
    shift_offset = _parse_offset(stack_shift)

    def _stack_box(box_name, box_offset, box_opacity, box_caption=" ", labels=False):
        xlabel = r'{{"MHSA", "MLP"}}' if labels else r'{{"", ""}}'
        ylabel = "D={}".format(embed_dim) if labels else ""
        zlabel = "N={}".format(token_count) if labels else ""
        return r"""
\pic[shift={ """+ _format_offset(box_offset) +""" }] at """+ to +"""
    {RightBandedBox={
        name="""+ box_name +""",
        caption="""+ _normalize_caption(box_caption) +""",
        xlabel="""+ xlabel +""",
        ylabel="""+ ylabel +""",
        zlabel="""+ zlabel +r""",
        fill=\TokenColor,
        bandfill=\AttentionColor,
        opacity="""+ str(box_opacity) +""",
        bandopacity="""+ str(min(box_opacity + 0.14, 0.88)) +""",
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

    parts = []
    for index in range(stack - 1, 0, -1):
        shadow_offset = tuple(base_offset[axis] + shift_offset[axis] * index for axis in range(3))
        shadow_opacity = max(opacity - 0.13 * index, 0.2)
        parts.append(
            _stack_box(
                box_name="{}_shadow{}".format(name, index),
                box_offset=shadow_offset,
                box_opacity=shadow_opacity,
            )
        )

    if caption is None or not str(caption).strip():
        caption_text = "{}"
    else:
        caption_text = "{}\\\\$\\times {}$".format(caption, layers)
    parts.append(
        _stack_box(
            box_name=name,
            box_offset=base_offset,
            box_opacity=opacity,
            box_caption=caption_text,
            labels=True,
        )
    )
    return "".join(parts)


def to_feature_reconstruct(name, spatial_size=14, out_channels=512, offset="(0,0,0)", to="(0,0,0)", width=(1.2, 1.0), height=12, depth=12, opacity=0.6, caption=r"Feature\\Reconstruct"):
    caption_text = _normalize_caption(caption)
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +"""
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption_text +""",
        xlabel={{"Reshape", "Proj"}},
        ylabel=C="""+ str(out_channels) +r""",
        zlabel="""+ str(spatial_size) +r"x" + str(spatial_size) + r""",
        fill=\ReconstructColor,
        bandfill=\ConvColor,
        opacity="""+ str(opacity) +""",
        bandopacity="""+ str(min(opacity + 0.12, 0.85)) +""",
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""


def to_mha(name, s_filer=16, n_filer=768, offset="(0,0,0)", to="(0,0,0)", width=2.2, height=11, depth=11, opacity=0.5, caption="MHA"):
    return to_ConvRes(
        name=name,
        s_filer=s_filer,
        n_filer=n_filer,
        offset=offset,
        to=to,
        width=width,
        height=height,
        depth=depth,
        opacity=opacity,
        caption=caption,
    )


def to_cross_attention(name, s_filer=32, n_filer=256, offset="(0,0,0)", to="(0,0,0)", width=2.0, height=16, depth=16, opacity=0.55, caption="Cross\\nAttention"):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +"""
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer) +""", """+ str(n_filer) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\AttentionColor,
        bandfill=\TokenColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width={ """+ str(width) +""" , """+ str(width / 1.3) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""


def to_legend(entries, at="(0,0,0)", title="Legend"):
    legend_rows = [r"\textbf{" + title + r"} & \\"]
    for label, color in entries:
        legend_rows.append(
            r"\tikz \draw[draw=black, fill="
            + color
            + r", opacity=0.9] (0,0) rectangle +(0.35,0.18); & "
            + label
            + r"\\"
        )
    body = "\n".join(legend_rows)
    return (
        r"\node[draw, fill=white, rounded corners=2pt, inner sep=5pt, opacity=0.95] at "
        + at
        + " {\n"
        + r"    \footnotesize"
        + "\n"
        + r"    \begin{tabular}{ll}"
        + "\n"
        + body
        + "\n"
        + r"    \end{tabular}"
        + "\n};\n"
    )

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
     


