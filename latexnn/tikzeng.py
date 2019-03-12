import os
import logging

logger = logging.getLogger(__name__)


def to_head():
    pathlayers = os.path.join(os.path.dirname(__file__), 'static', '')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{""" + pathlayers + r"""}{init}
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
\def\SoftmaxColor{rgb:magenta,5;black,7}   
"""


def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""


def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_generate(arch, pathname="file.tex"):
    final_arch = [to_head(), to_cor(), to_begin()]
    final_arch.extend(arch)
    final_arch.append(to_end())
    with open(pathname, "w") as f:
        logger.info("Print architecture")
        for c in final_arch:
            if logger.getEffectiveLevel() < logging.WARNING:
                print(c)
            f.write(c)
    logger.critical("Run following command:\npdflatex {0}.tex && rm -f {0}.aux {0}.log {0}.vscodeLog {0}.tex".format(
        ".".join(pathname.split(".")[:-1])))


def to_pdf(arch, pathname="file.pdf"):
    target = ".".join(pathname.split(".")[:-1])
    tex = target + ".tex"
    to_generate(arch, tex)
    os.system("pdflatex %s" % tex)
    os.system("rm -rf {0}.aux {0}.log {0}.vscodeLog {0}.tex".format(target))
