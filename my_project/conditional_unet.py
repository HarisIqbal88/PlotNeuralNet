
import sys

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # ==================== 输入 ====================
    to_input('../examples/fcn8s/cats.jpg'),

    # ==================== 初始卷积层 ====================
    to_Conv(name="init_conv", s_filer=64, n_filer=64, offset="(0,0,0)",
            to="(0,0,0)", height=40, depth=40, width=2, caption="Init Conv"),

    # ==================== 下采样路径（Encoder） ====================
    # Down Block 1: 64 channels
    to_ConvConvRelu(name='down1', s_filer=64, n_filer=(64, 64), offset="(0,0,0)",
                    to="(init_conv-east)", width=(2, 2), height=40, depth=40, caption="Down1"),
    to_Pool(name="downsample1", offset="(0,0,0)", to="(down1-east)",
            width=1, height=32, depth=32, opacity=0.5),

    # Down Block 2: 128 channels
    *block_2ConvPool(name='d2', botton='downsample1', top='downsample2',
                     s_filer=128, n_filer=128, offset="(1,0,0)",
                     size=(32, 32, 3.5), opacity=0.5),

    # Down Block 3: 256 channels
    *block_2ConvPool(name='d3', botton='downsample2', top='downsample3',
                     s_filer=256, n_filer=256, offset="(1,0,0)",
                     size=(25, 25, 4.5), opacity=0.5),

    # Down Block 4: 512 channels
    *block_2ConvPool(name='d4', botton='downsample3', top='downsample4',
                     s_filer=512, n_filer=512, offset="(1,0,0)",
                     size=(16, 16, 5.5), opacity=0.5),

    # ==================== 中间层（Bottleneck） ====================
    # Mid1
    to_ConvConvRelu(name='mid1', s_filer=8, n_filer=(512, 512), offset="(1.5,0,0)",
                    to="(downsample4-east)", width=(8, 8), height=8, depth=8, caption="Mid1"),
    to_connection("downsample4", "mid1"),

    # Attention Block
    to_Conv(name='mid_attn', s_filer=8, n_filer=512, offset="(0.8,0,0)",
            to="(mid1-east)", height=8, depth=8, width=8, caption="Attention"),
    to_connection("mid1", "mid_attn"),

    # Mid2
    to_ConvConvRelu(name='mid2', s_filer=8, n_filer=(512, 512), offset="(0.8,0,0)",
                    to="(mid_attn-east)", width=(8, 8), height=8, depth=8, caption="Bottleneck"),
    to_connection("mid_attn", "mid2"),

    # ==================== 上采样路径（Decoder） ====================
    # Up Block 1: 256 channels (concatenate with down3)
    *block_Unconv(name="u1", botton="mid2", top='u1_end', s_filer=16, n_filer=256,
                  offset="(1.8,0,0)", size=(16, 16, 5.0), opacity=0.5),
    to_skip(of='ccr_d3', to='ccr_res_u1', pos=1.25),

    # Up Block 2: 128 channels (concatenate with down2)
    *block_Unconv(name="u2", botton="u1_end", top='u2_end', s_filer=32, n_filer=128,
                  offset="(1.8,0,0)", size=(25, 25, 4.5), opacity=0.5),
    to_skip(of='ccr_d2', to='ccr_res_u2', pos=1.25),

    # Up Block 3: 64 channels (concatenate with down1)
    *block_Unconv(name="u3", botton="u2_end", top='u3_end', s_filer=64, n_filer=64,
                  offset="(1.8,0,0)", size=(32, 32, 3.5), opacity=0.5),
    to_skip(of='down1', to='ccr_res_u3', pos=1.25),

    # Up Block 4: 64 channels (no skip connection)
    to_ConvConvRelu(name='up4', s_filer=64, n_filer=(64, 64), offset="(1.5,0,0)",
                    to="(u3_end-east)", width=(2, 2), height=40, depth=40, caption="Up4"),
    to_connection("u3_end", "up4"),

    # ==================== 最终输出 ====================
    # Instance Normalization
    to_Conv(name="final_norm", s_filer=64, n_filer=64, offset="(0.75,0,0)",
            to="(up4-east)", height=40, depth=40, width=1, caption="InstanceNorm"),
    to_connection("up4", "final_norm"),

    # Output Convolution
    to_SoftMax(name="output", s_filer=64, offset="(0.75,0,0)",
               to="(final_norm-east)", caption="Output"),
    to_connection("final_norm", "output"),

    # ==================== 时间与条件嵌入标注 ====================
    # 添加文本标注说明时间步和条件嵌入
    to_Conv(name="time_emb_label", s_filer=256, n_filer=256, offset="(0,5,0)",
            to="(init_conv-north)", height=15, depth=15, width=1, caption="Time\\\\Embedding"),
    to_Conv(name="cond_emb_label", s_filer=256, n_filer=256, offset="(3,5,0)",
            to="(init_conv-north)", height=15, depth=15, width=1, caption="Condition\\\\Embedding"),

    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
