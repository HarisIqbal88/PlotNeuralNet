import sys

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *


arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    to_input('../examples/fcn8s/cats.jpg'),

    # Encoder
    to_ConvConvRelu(name='enc_b1', s_filer=512, n_filer=(64, 64), offset='(0,0,0)', to='(0,0,0)', width=(2, 2), height=40, depth=40),
    to_Pool(name='pool_b1', offset='(0,0,0)', to='(enc_b1-east)', width=1, height=32, depth=32, opacity=0.5),
    *block_unet_stage(name='b2', botton='pool_b1', top='pool_b2', s_filer=256, n_filer=128, offset='(1,0,0)', size=(32, 32, 3.5), pool=True, opacity=0.5),
    *block_unet_stage(name='b3', botton='pool_b2', top='pool_b3', s_filer=128, n_filer=256, offset='(1,0,0)', size=(24, 24, 4.2), pool=True, opacity=0.5),
    *block_unet_stage(name='b4', botton='pool_b3', top='pool_b4', s_filer=64, n_filer=512, offset='(1,0,0)', size=(16, 16, 5.0), pool=True, opacity=0.5),

    to_ConvConvRelu(name='bottleneck', s_filer=32, n_filer=(1024, 1024), offset='(1.8,0,0)', to='(pool_b4-east)', width=(7, 7), height=9, depth=9, caption='Bottleneck'),
    to_connection('pool_b4', 'bottleneck'),

    # Attention gates for skip tensors
    *block_attention_gate(name='g4', g='bottleneck', x='enc_b4', top='gated_b4', s_filer=64, n_filer=512, gate_offset='(0.6,1.1,0)', out_offset='(0.5,0,0)', size=(14, 14, 2.0)),
    *to_upsample_concat(name='d4', botton='bottleneck', skip='gated_b4', top='dec_b4', s_filer=64, n_filer=512, offset='(1.8,0,0)', size=(16, 16, 4.6), opacity=0.5),

    *block_attention_gate(name='g3', g='dec_b4', x='enc_b3', top='gated_b3', s_filer=128, n_filer=256, gate_offset='(0.6,1.0,0)', out_offset='(0.5,0,0)', size=(19, 19, 1.9)),
    *to_upsample_concat(name='d3', botton='dec_b4', skip='gated_b3', top='dec_b3', s_filer=128, n_filer=256, offset='(1.6,0,0)', size=(24, 24, 3.8), opacity=0.5),

    *block_attention_gate(name='g2', g='dec_b3', x='enc_b2', top='gated_b2', s_filer=256, n_filer=128, gate_offset='(0.6,1.0,0)', out_offset='(0.5,0,0)', size=(25, 25, 1.8)),
    *to_upsample_concat(name='d2', botton='dec_b3', skip='gated_b2', top='dec_b2', s_filer=256, n_filer=128, offset='(1.5,0,0)', size=(32, 32, 3.2), opacity=0.5),

    *block_attention_gate(name='g1', g='dec_b2', x='enc_b1', top='gated_b1', s_filer=512, n_filer=64, gate_offset='(0.6,1.0,0)', out_offset='(0.5,0,0)', size=(32, 32, 1.7)),
    *to_upsample_concat(name='d1', botton='dec_b2', skip='gated_b1', top='dec_b1', s_filer=512, n_filer=64, offset='(1.4,0,0)', size=(40, 40, 2.4), opacity=0.5),

    to_ConvSoftMax(name='seg', s_filer=512, offset='(0.8,0,0)', to='(dec_b1-east)', width=1.0, height=40, depth=40, caption='Mask'),
    to_connection('dec_b1', 'seg'),
    to_end(),
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()

