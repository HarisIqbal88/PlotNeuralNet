import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pycore.blocks import block_transunet_bridge
from pycore.tikzeng import (
    to_Conv,
    to_ConvConvRelu,
    to_ConvSoftMax,
    to_Pool,
    to_UnPool,
    to_begin,
    to_connection,
    to_cor,
    to_end,
    to_generate,
    to_head,
    to_legend,
    to_skip_v2,
    to_text,
)


LABEL_STYLE = (
    r"font=\bfseries\small, align=center, fill=white, fill opacity=0.9, "
    r"text opacity=1, rounded corners=2pt, inner sep=2pt"
)

BOTTOM_LABEL_STYLE = (
    r"font=\scriptsize, align=center, fill=white, fill opacity=0.92, "
    r"text opacity=1, rounded corners=1pt, inner sep=1.5pt"
)


def extend_arch(arch, items):
    arch.extend(items)


def main():
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tex_path = os.path.join(os.path.dirname(__file__), "transunet.tex")

    arch = [
        to_head(project_path),
        to_cor(),
        to_begin(),
        to_Conv(
            name="input",
            s_filer="224x224",
            n_filer="3",
            to="(-7.0,0,0)",
            width=1.8,
            height=25,
            depth=25,
            caption=" ",
        ),
        to_ConvConvRelu(
            name="enc1",
            s_filer="112x112",
            n_filer=(64, 64),
            offset="(2.3,0,0)",
            to="(input-east)",
            width=(1.4, 1.4),
            height=25,
            depth=25,
            caption=" ",
        ),
        to_connection("input", "enc1"),
        to_Pool(
            name="pool1",
            offset="(0,0,0)",
            to="(enc1-east)",
            width=1,
            height=21,
            depth=21,
            opacity=0.5,
            caption=" ",
        ),
        to_connection("enc1", "pool1"),
        to_ConvConvRelu(
            name="enc2",
            s_filer="56x56",
            n_filer=(128, 128),
            offset="(1.6,0,0)",
            to="(pool1-east)",
            width=(1.5, 1.5),
            height=21,
            depth=21,
            caption=" ",
        ),
        to_connection("pool1", "enc2"),
        to_Pool(
            name="pool2",
            offset="(0,0,0)",
            to="(enc2-east)",
            width=1,
            height=17,
            depth=17,
            opacity=0.5,
            caption=" ",
        ),
        to_connection("enc2", "pool2"),
        to_ConvConvRelu(
            name="enc3",
            s_filer="28x28",
            n_filer=(256, 256),
            offset="(1.6,0,0)",
            to="(pool2-east)",
            width=(1.6, 1.6),
            height=17,
            depth=17,
            caption=" ",
        ),
        to_connection("pool2", "enc3"),
        to_Pool(
            name="pool3",
            offset="(0,0,0)",
            to="(enc3-east)",
            width=1,
            height=13,
            depth=13,
            opacity=0.5,
            caption=" ",
        ),
        to_connection("enc3", "pool3"),
        to_ConvConvRelu(
            name="enc4",
            s_filer="14x14",
            n_filer=(512, 512),
            offset="(1.6,0,0)",
            to="(pool3-east)",
            width=(1.7, 1.7),
            height=13,
            depth=13,
            caption=" ",
        ),
        to_connection("pool3", "enc4"),
    ]

    extend_arch(
        arch,
        block_transunet_bridge(
            name="bridge",
            botton="enc4",
            top="reconstruct",
            feature_size=14,
            token_count=196,
            embed_dim=768,
            out_channels=512,
            patch_offset="(1.8,0,0)",
            token_offset="(1.5,0,0)",
            recon_offset="(1.55,0,0)",
            patch_size=(12, 12, (1.15, 1.15)),
            token_size=(13, 13, (1.55, 1.55)),
            recon_size=(12, 12, (1.35, 1.1)),
            layers=12,
            patch_caption="",
            token_caption="",
            recon_caption="",
        ),
    )

    arch.extend(
        [
            to_UnPool(
                name="up3",
                offset="(1.7,0,0)",
                to="(reconstruct-east)",
                width=1,
                height=17,
                depth=17,
                opacity=0.55,
                caption=" ",
            ),
            to_connection("reconstruct", "up3"),
            to_ConvConvRelu(
                name="dec3",
                s_filer="28x28",
                n_filer=(256, 256),
                offset="(0.9,0,0)",
                to="(up3-east)",
                width=(1.6, 1.6),
                height=17,
                depth=17,
                caption=" ",
            ),
            to_connection("up3", "dec3"),
            to_UnPool(
                name="up2",
                offset="(1.5,0,0)",
                to="(dec3-east)",
                width=1,
                height=21,
                depth=21,
                opacity=0.55,
                caption=" ",
            ),
            to_connection("dec3", "up2"),
            to_ConvConvRelu(
                name="dec2",
                s_filer="56x56",
                n_filer=(128, 128),
                offset="(0.9,0,0)",
                to="(up2-east)",
                width=(1.5, 1.5),
                height=21,
                depth=21,
                caption=" ",
            ),
            to_connection("up2", "dec2"),
            to_UnPool(
                name="up1",
                offset="(1.5,0,0)",
                to="(dec2-east)",
                width=1,
                height=25,
                depth=25,
                opacity=0.55,
                caption=" ",
            ),
            to_connection("dec2", "up1"),
            to_ConvConvRelu(
                name="dec1",
                s_filer="112x112",
                n_filer=(64, 64),
                offset="(0.9,0,0)",
                to="(up1-east)",
                width=(1.4, 1.4),
                height=25,
                depth=25,
                caption=" ",
            ),
            to_connection("up1", "dec1"),
            to_ConvSoftMax(
                name="seg",
                s_filer="224x224",
                offset="(1.8,0,0)",
                to="(dec1-east)",
                width=1.7,
                height=25,
                depth=25,
                caption=" ",
            ),
            to_connection("dec1", "seg"),
            to_skip_v2(of="enc1", to="dec1", pos=1.86),
            to_skip_v2(of="enc2", to="dec2", pos=1.63),
            to_skip_v2(of="enc3", to="dec3", pos=1.42),
            to_text("input_label", r"Input\\Layer", to=r"($(input-anchor)+(0,3.7,0)$)", style=LABEL_STYLE),
            to_text("encoder_label", r"CNN\\Encoder", to=r"($(enc2-anchor)!0.5!(enc4-anchor)+(0,4.2,0)$)", style=LABEL_STYLE),
            to_text("patch_label", r"Patch\\Embedding", to=r"($(bridge_patch-anchor)+(0,3.7,0)$)", style=LABEL_STYLE),
            to_text("transformer_label", r"Transformer\\Encoder", to=r"($(bridge_transformer-anchor)+(0,4.3,0)$)", style=LABEL_STYLE),
            to_text("reconstruct_label", r"Feature\\Reconstruction", to=r"($(reconstruct-anchor)+(0,3.9,0)$)", style=LABEL_STYLE),
            to_text("decoder_label", r"U-Net\\Decoder", to=r"($(dec3-anchor)!0.5!(dec1-anchor)+(0,4.2,0)$)", style=LABEL_STYLE),
            to_text("skip_label", r"Skip\\Connections", to=r"($(enc2-anchor)!0.5!(dec2-anchor)+(0,6.2,0)$)", style=LABEL_STYLE),
            to_text("seg_label", r"Segmentation\\Head", to=r"($(seg-anchor)+(0,3.7,0)$)", style=LABEL_STYLE),
            to_text("input_note", r"Input", to=r"($(input-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("enc1_note", r"Enc1", to=r"($(enc1-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("enc2_note", r"Enc2", to=r"($(enc2-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("enc3_note", r"Enc3", to=r"($(enc3-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("enc4_note", r"Hybrid\\CNN", to=r"($(enc4-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("patch_note", r"Patch\\Embed", to=r"($(bridge_patch-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("transformer_note", r"Encoder\\Layer\\$\times 12$", to=r"($(bridge_transformer-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("reconstruct_note", r"Reshape\\Proj", to=r"($(reconstruct-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("dec3_note", r"Dec3", to=r"($(dec3-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("dec2_note", r"Dec2", to=r"($(dec2-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("dec1_note", r"Dec1", to=r"($(dec1-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_text("seg_note", r"1x1\\Conv", to=r"($(seg-anchor)+(0,-5.0,0)$)", style=BOTTOM_LABEL_STYLE),
            to_legend(
                entries=[
                    ("CNN Encoder / Decoder", "\\ConvColor"),
                    ("Down / Up Sampling", "\\PoolColor"),
                    ("Patch Embedding", "\\PatchEmbedColor"),
                    ("Transformer Encoder", "\\TokenColor"),
                    ("Feature Reconstruction", "\\ReconstructColor"),
                    ("Segmentation Head", "\\SoftmaxColor"),
                ],
                at="(18.5,-7.2,0)",
                title="TransUNet",
            ),
            to_end(),
        ]
    )

    to_generate(arch, pathname=tex_path)


if __name__ == "__main__":
    main()
