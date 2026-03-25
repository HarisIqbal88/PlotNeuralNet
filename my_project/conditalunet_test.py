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

    # ==================== 初始卷积 + Down1 ====================
    # init_conv: Conv2d(in_channels, base_channels)
    to_ConvConvRelu(
        name='init', s_filer=512, n_filer=(64, 64),
        offset="(0,0,0)", to="(0,0,0)",
        width=(2, 2), height=40, depth=40, caption="InitConv"
    ),

    # down1: ResidualBlock(base, base)，后接 Downsample(base)
    to_ConvConvRelu(
        name='ccr_b1', s_filer=512, n_filer=(64, 64),
        offset="(0,0,0)", to="(init-east)",
        width=(2, 2), height=40, depth=40, caption="Down1"
    ),
    to_Pool(
        name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)",
        width=1, height=32, depth=32, opacity=0.5
    ),

    # ==================== Down2：ResidualBlock(base, 2*base) + Downsample(2*base) ====================
    *block_2ConvPool(
        name='b2', botton='pool_b1', top='pool_b2',
        s_filer=256, n_filer=128,  # 64 -> 128
        offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5
    ),

    # ==================== Down3：ResidualBlock(2*base, 2*base) + Downsample(2*base) ====================
    *block_2ConvPool(
        name='b3', botton='pool_b2', top='pool_b3',
        s_filer=128, n_filer=128,  # 128 -> 128
        offset="(1,0,0)", size=(25, 25, 4.5), opacity=0.5
    ),

    # ==================== Down4：ResidualBlock(2*base, 4*base)，无下采样 ====================
    to_ConvConvRelu(
        name='ccr_b4', s_filer=64, n_filer=(256, 256),  # 128 -> 256
        offset="(1,0,0)", to="(pool_b3-east)",
        width=(5, 5), height=16, depth=16, caption="Down4"
    ),

    # ==================== Bottleneck：mid1 + Attention + mid2 ====================
    # mid1: ResidualBlock(4*base, 4*base)
    to_ConvConvRelu(
        name='ccr_mid1', s_filer=32, n_filer=(256, 256),
        offset="(2,0,0)", to="(ccr_b4-east)",
        width=(8, 8), height=8, depth=8, caption="Mid1"
    ),
    to_connection("ccr_b4", "ccr_mid1"),

    # mid_attn: AttentionBlock(4*base)
    to_ConvConvRelu(
        name='ccr_mid_attn', s_filer=32, n_filer=(256, 256),
        offset="(0.8,0,0)", to="(ccr_mid1-east)",
        width=(8, 8), height=8, depth=8, caption="MidAttn"
    ),
    to_connection("ccr_mid1", "ccr_mid_attn"),

    # mid2: ResidualBlock(4*base, 4*base)
    to_ConvConvRelu(
        name='ccr_mid2', s_filer=32, n_filer=(256, 256),
        offset="(0.8,0,0)", to="(ccr_mid_attn-east)",
        width=(8, 8), height=8, depth=8, caption="Mid2"
    ),
    to_connection("ccr_mid_attn", "ccr_mid2"),

    # ==================== Up1：upsample1 + concat(h3) + up1 ====================
    # Upsample(base*4) 后通道仍近似 256，尺寸翻倍
    *block_Unconv(
        name="u1", botton="ccr_mid2", top='end_u1',
        s_filer=64, n_filer=256,  # 对应 upsample1 + up1 输出大约 2*base
        offset="(2.1,0,0)", size=(16, 16, 5.0), opacity=0.5
    ),
    # skip：来自 h3（down3 输出，对应 ccr_b3）
    to_skip(of='ccr_b3', to='ccr_res_u1', pos=0.5),

    # ==================== Up2：upsample2 + concat(h2) + up2 ====================
    *block_Unconv(
        name="u2", botton="end_u1", top='end_u2',
        s_filer=128, n_filer=128,  # 输出约 2*base
        offset="(2.1,0,0)", size=(25, 25, 4.5), opacity=0.5
    ),
    # skip：来自 h2（down2 输出，对应 ccr_b2）
    to_skip(of='ccr_b2', to='ccr_res_u2', pos=0.5),

    # ==================== Up3：upsample3 + concat(h1) + up3 ====================
    *block_Unconv(
        name="u3", botton="end_u2", top='end_u3',
        s_filer=256, n_filer=64,  # 输出 base
        offset="(2.1,0,0)", size=(32, 32, 3.5), opacity=0.5
    ),
    # skip：来自 h1（down1 输出，对应 ccr_b1）
    to_skip(of='ccr_b1', to='ccr_res_u3', pos=0.5),

    # ==================== Up4：up4（不再上采样） ====================
    to_ConvConvRelu(
        name='ccr_u4', s_filer=512, n_filer=(64, 64),
        offset="(2.1,0,0)", to="(end_u3-east)",
        width=(2, 2), height=40, depth=40, caption="Up4"
    ),
    to_connection("end_u3", "ccr_u4"),

    # ==================== 最终输出：final_norm + final_conv ====================
    # final_norm: InstanceNorm2d(base_channels)
    to_Conv(
        name="final_norm", s_filer=512, n_filer=64,
        offset="(0.75,0,0)", to="(ccr_u4-east)",
        width=1, height=40, depth=40, caption="InstNorm"
    ),
    to_connection("ccr_u4", "final_norm"),

    # final_conv: Conv2d(base_channels, in_channels)
    to_ConvSoftMax(
        name="final_conv", s_filer=512,
        offset="(0.75,0,0)", to="(final_norm-east)",
        width=1, height=40, depth=40, caption="OutConv"
    ),
    to_connection("final_norm", "final_conv"),

    # ==================== 顶部：时间 / 条件嵌入（示意块） ====================
    to_ConvConvRelu(
        name="time_emb", s_filer=256, n_filer=(256, 256),
        offset="(0,4,0)", to="(ccr_mid1-north)",
        width=(1, 1), height=15, depth=15, caption="TimeEmb"
    ),
    to_ConvConvRelu(
        name="cond_emb", s_filer=256, n_filer=(256, 256),
        offset="(2,0,0)", to="(time_emb-east)",
        width=(1, 1), height=15, depth=15, caption="CondEmb"
    ),

    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
