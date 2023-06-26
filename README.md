# PlotNeuralNet

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2526396.svg)](https://doi.org/10.5281/zenodo.2526396)

Latex code for drawing neural networks for reports and presentation. Have a look into examples to see how they are made. Additionally, lets consolidate any improvements that you make and fix any bugs to help more people with this code.

## Examples

Following are some network representations:

<p align="center"><img  src="https://user-images.githubusercontent.com/17570785/50308846-c2231880-049c-11e9-8763-3daa1024de78.png" width="85%" height="85%"></p>
<h6 align="center">FCN-8 (<a href="https://www.overleaf.com/read/kkqntfxnvbsk">view on Overleaf</a>)</h6>

<p align="center"><img  src="https://user-images.githubusercontent.com/17570785/50308873-e2eb6e00-049c-11e9-9587-9da6bdec011b.png" width="85%" height="85%"></p>
<h6 align="center">FCN-32 (<a href="https://www.overleaf.com/read/wsxpmkqvjnbs">view on Overleaf</a>)</h6>

<p align="center"><img  src="https://user-images.githubusercontent.com/17570785/50308911-03b3c380-049d-11e9-92d9-ce15669017ad.png" width="85%" height="85%"></p>
<h6 align="center">Holistically-Nested Edge Detection (<a href="https://www.overleaf.com/read/jxhnkcnwhfxp">view on Overleaf</a>)</h6>

## Getting Started

1. Install the following packages on Ubuntu.

* Ubuntu 16.04

```sh
sudo apt-get install texlive-latex-extra


```

* Ubuntu 18.04.2
   Base on this [website](https://gist.github.com/rain1024/98dd5e2c6c8c28f9ea9d), please install the following packages.

```sh
sudo apt-get install texlive-latex-base
sudo apt-get install texlive-fonts-recommended
sudo apt-get install texlive-fonts-extra
sudo apt-get install texlive-latex-extra


```

* Windows

1. Download and install [MikTeX](https://miktex.org/download).
2. Download and install bash runner on Windows, recommends [Git bash](https://git-scm.com/download/win) or Cygwin(https://www.cygwin.com/)
3. Execute the example as followed.

```sh
cd pyexamples/
bash ../tikzmake.sh test_simple

```

* Docker

1. Install [Docker](https://www.docker.com/). If using Windows, you can install Docker Desktop for Windows, or use WSL to install Docker CE for Ubuntu.

   - The MikTex docker image is used as the base stage for the docker build, which is based on Ubuntu 20.04 LTS

2. Run the `docker_build.sh` file using the following command to build the docker image (from the root directory of this repo). You need bash to run this script. If using Windows, you can install Git bash or Cygwin; WSL and Linux have bash built-in.

```sh
bash build_pnn_docker.sh

```

3. Run the container in docker (from a WSL or Linux terminal) with the following command (from the root directory of this repo). Ensure the command is being run as admin of the machine.

```sh
bash start_pnn_docker.sh

```

## TODO

- [X] Python interface
- [ ] Add easy legend functionality
- [ ] Add more layer shapes like TruncatedPyramid, 2DSheet etc
- [ ] Add examples for RNN and likes.

## Latex usage

See [`examples`](examples) directory for usage.

## Python usage

First, create a new directory and a new Python file:

    $ mkdir my_project
    $ cd my_project
    vim my_arch.py

Add the following code to your new file:

```python
import sys
sys.path.append('../')
from pycore.tikzeng import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_Conv("conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2 ),
    to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)"),
    to_Conv("conv2", 128, 64, offset="(1,0,0)", to="(pool1-east)", height=32, depth=32, width=2 ),
    to_connection( "pool1", "conv2"),
    to_Pool("pool2", offset="(0,0,0)", to="(conv2-east)", height=28, depth=28, width=1),
    to_SoftMax("soft1", 10 ,"(3,0,0)", "(pool1-east)", caption="SOFT"  ),
    to_connection("pool2", "soft1"),
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()


```

Now, run the program as follows:

    bash ../tikzmake.sh my_arch

## Poetry Dependency Management

To use in other projects that use Poetry for dependency management, add the following to your `pyproject.toml` file:

```toml
[tool.poetry.dev-dependencies]
plotneuralnet           = { git = "https://github.com/HarisIqbal88/PlotNeuralNet.git" }
```



