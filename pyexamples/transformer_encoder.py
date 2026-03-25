import sys

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *


arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    to_Conv(
        name='input',
        s_filer=224,
        n_filer=3,
        offset='(0,0,0)',
        to='(0,0,0)',
        width=1.2,
        height=36,
        depth=36,
        caption='Input\nImage',
    ),

    *block_transformer_encoder(
        name='vit',
        botton='input',
        top='vit_encoder',
        s_filer=14,
        n_filer=768,
        patch_size=16,
        patch_offset='(1.5,0,0)',
        token_offset='(1.0,0,0)',
        size=(12, 12, 4.0),
        layers=12,
    ),

    to_mha(
        name='mha_detail',
        s_filer=14,
        n_filer=768,
        offset='(1.6,1.1,0)',
        to='(vit_encoder-east)',
        width=2.3,
        height=10,
        depth=10,
        opacity=0.45,
        caption='MHA + MLP',
    ),
    to_connection_anchor('vit_encoder', 'mha_detail', src_anchor='northeast', dst_anchor='west'),

    to_ConvSoftMax(
        name='cls_head',
        s_filer=1,
        offset='(1.6,0,0)',
        to='(vit_encoder-east)',
        width=1.2,
        height=8,
        depth=8,
        caption='CLS',
    ),
    to_connection('vit_encoder', 'cls_head'),

    to_end(),
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()

