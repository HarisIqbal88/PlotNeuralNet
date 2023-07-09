from torch import th
from torchinfo import summary

import pycore.tikzeng as pnn


class TorchArchParser:
    """Parse a torch module to a tikz architecture diagram.

    Currently supported torch modules:
        - Layers: Linear
        - Activations: ReLU
    """

    text_mapping = {
        "Linear": r"\\mathrm{{FC}}",
        "ReLU": r"\\varphi_\\mathrm{{ReLU}}"
    }

    def __init__(self, torch_module: th.nn.Module, input_size):

        assert isinstance(torch_module, th.nn.Module), "torch_module is not an instance of torch.nn.Module."

        self.torch_module = torch_module

        self.summary_list = summary(self.torch_module, input_size=input_size).summary_list

        self.arch = self.parse(self.summary_list)

    def get_arch(self):
        return self.arch

    @staticmethod
    def parse(summary_list):
        arch = list()
        arch.append(pnn.to_head(".."))
        arch.append(pnn.to_cor())
        arch.append(pnn.to_begin())
        for idx, layer in enumerate(summary_list[2:], start=1):
            if layer.class_name == "Linear":
                text = TorchArchParser.text_mapping.get(layer.class_name, "\\mathrm{{FC}}")
                arch_layer = pnn.to_Conv(
                    name=f"module{idx}",
                    s_filer="",
                    n_filer=layer.module.out_features,
                    offset=str((1, 0, 0)),
                    width=1,
                    height=layer.module.out_features,
                    depth=1,
                    fill_color="\\FcColor",
                    caption=f"${text}$",
                    to=f"(module{idx-1}-east)" if idx > 1 else str((0, 0, 0)),
                )
                arch.append(arch_layer)

                if idx > 1:
                    arch_layer = pnn.to_connection(f"module{idx-1}", f"module{idx}")
                    arch.append(arch_layer)

            elif layer.class_name in {"ReLU"}:
                text = TorchArchParser.text_mapping.get(layer.class_name, "\\varphi")
                arch_layer = pnn.to_Conv(
                    name=f"module{idx}",
                    s_filer="",
                    n_filer="",
                    offset=str((0.5, 0, 0)),
                    width=0.5,
                    height=layer.input_size[1],
                    depth=layer.input_size[0],
                    caption=f"${text}$",
                    to=f"(module{idx-1}-east)" if idx > 1 else str((0, 0, 0)),
                )
                arch.append(arch_layer)

            else:
                raise NotImplementedError(f"Layer {layer.class_name} is not supported, yet.")

        arch.append(pnn.to_end())

        return arch
