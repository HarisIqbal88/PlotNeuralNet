
from .tikzeng import *

#define new block
def block_2ConvPool( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
    to_ConvConvRelu( 
        name="ccr_{}".format( name ),
        s_filer=str(s_filer), 
        n_filer=(n_filer,n_filer), 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=(size[2],size[2]), 
        height=size[0], 
        depth=size[1],   
        ),    
    to_Pool(         
        name="{}".format( top ), 
        offset="(0,0,0)", 
        to="(ccr_{}-east)".format( name ),  
        width=1,         
        height=size[0] - int(size[0]/4), 
        depth=size[1] - int(size[0]/4), 
        opacity=opacity, ),
    to_connection( 
        "{}".format( botton ), 
        "ccr_{}".format( name )
        )
    ]


def block_Unconv( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=1,              height=size[0],       depth=size[1], opacity=opacity ),
        to_ConvRes( name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),    s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_ConvRes( name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),       s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='{}'.format(top),            offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name), s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]




def block_Res( num, name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5 ):
    lys = []
    layers = [ *[ '{}_{}'.format(name,i) for i in range(num-1) ], top]
    for name in layers:        
        ly = [ to_Conv( 
            name='{}'.format(name),       
            offset=offset, 
            to="({}-east)".format( botton ),   
            s_filer=str(s_filer), 
            n_filer=str(n_filer), 
            width=size[2],
            height=size[0],
            depth=size[1]
            ),
            to_connection( 
                "{}".format( botton  ), 
                "{}".format( name ) 
                )
            ]
        botton = name
        lys+=ly
    
    lys += [
        to_skip( of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


# helper to flatten nested list structures
def _flatten_arch(items):
    arch = []
    for item in items:
        if isinstance(item, list):
            arch.extend(item)
        else:
            arch.append(item)
    return arch


def block_unet_stage(name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32, 32, 3.5), pool=True, opacity=0.5, caption=""):
    conv_name = "enc_{}".format(name)
    layers = [
        to_ConvConvRelu(
            name=conv_name,
            s_filer=s_filer,
            n_filer=(n_filer, n_filer),
            offset=offset,
            to="({}-east)".format(botton),
            width=(size[2], size[2]),
            height=size[0],
            depth=size[1],
            caption=caption,
        ),
        to_connection(botton, conv_name),
    ]
    if pool:
        layers.append(
            to_Pool(
                name=top,
                offset="(0,0,0)",
                to="({}-east)".format(conv_name),
                width=1,
                height=size[0] - int(size[0] / 4),
                depth=size[1] - int(size[1] / 4),
                opacity=opacity,
            )
        )
    return layers


def block_transformer_encoder(name, botton, top, s_filer=16, n_filer=768, patch_size=16, patch_offset="(1.4,0,0)", token_offset="(1.0,0,0)", size=(12, 12, 3.8), layers=12):
    patch_name = "patch_{}".format(name)
    token_name = top
    return [
        to_patch_embed(
            name=patch_name,
            s_filer=s_filer,
            n_filer=n_filer,
            offset=patch_offset,
            to="({}-east)".format(botton),
            width=2.0,
            height=size[0],
            depth=size[1],
            caption="Patch {}x{}".format(patch_size, patch_size),
        ),
        to_connection(botton, patch_name),
        to_token_block(
            name=token_name,
            s_filer=s_filer,
            n_filer=n_filer,
            offset=token_offset,
            to="({}-east)".format(patch_name),
            width=size[2],
            height=size[0] + 1,
            depth=size[1] + 1,
            caption="Transformer x{}".format(layers),
        ),
        to_connection(patch_name, token_name),
    ]


def block_transunet_bridge(name, botton, top, feature_size=14, token_count=196, embed_dim=768, out_channels=512, patch_offset="(1.6,0,0)", token_offset="(1.35,0,0)", recon_offset="(1.45,0,0)", patch_size=(12, 12, (1.15, 1.15)), token_size=(13, 13, (1.55, 1.55)), recon_size=(12, 12, (1.2, 1.0)), layers=12, patch_caption=r"Patch\\Embed", token_caption=r"Encoder\\Layer", recon_caption=r"Reshape\\Proj"):
    patch_name = "{}_patch".format(name)
    token_name = "{}_transformer".format(name)
    return [
        to_patch_embedding(
            name=patch_name,
            token_count=token_count,
            embed_dim=embed_dim,
            offset=patch_offset,
            to="({}-east)".format(botton),
            width=patch_size[2],
            height=patch_size[0],
            depth=patch_size[1],
            caption=patch_caption,
        ),
        to_connection(botton, patch_name),
        to_transformer_encoder_stack(
            name=token_name,
            token_count=token_count,
            embed_dim=embed_dim,
            offset=token_offset,
            to="({}-east)".format(patch_name),
            width=token_size[2],
            height=token_size[0],
            depth=token_size[1],
            layers=layers,
            caption=token_caption,
        ),
        to_connection(patch_name, token_name),
        to_feature_reconstruct(
            name=top,
            spatial_size=feature_size,
            out_channels=out_channels,
            offset=recon_offset,
            to="({}-east)".format(token_name),
            width=recon_size[2],
            height=recon_size[0],
            depth=recon_size[1],
            caption=recon_caption,
        ),
        to_connection(token_name, top),
    ]


def block_transunet_cross_attn_decoder(name, botton, skip, top, s_filer=32, n_filer=256, offset="(1.5,0,0)", size=(18, 18, 2.4), qkv_size=(8, 8, 1.1), opacity=0.5):
    up_name = "{}_up".format(name)
    q_name = "{}_q".format(name)
    kv_name = "{}_kv".format(name)
    k_name = "{}_k".format(name)
    v_name = "{}_v".format(name)
    xca_name = "{}_xca".format(name)
    add_name = "{}_add".format(name)

    return [
        to_UnPool(name=up_name, offset=offset, to="({}-east)".format(botton), width=1, height=size[0], depth=size[1], opacity=opacity, caption="Up"),
        to_connection(botton, up_name),
        # Query branch (top lane)
        to_ConvRes(name=q_name, s_filer=s_filer, n_filer=n_filer, offset="(0.9,1.05,0)", to="({}-east)".format(up_name), width=qkv_size[2], height=qkv_size[0], depth=qkv_size[1], opacity=0.5, caption="Q", fill='\\QColor', bandfill='\\QColor'),
        to_connection_anchor(up_name, q_name, src_anchor="northeast", dst_anchor="west"),
        # Skip branch (bottom lane), then split into K/V.
        to_ConvRes(name=kv_name, s_filer=s_filer, n_filer=n_filer, offset="(0.85,-1.05,0)", to="({}-east)".format(up_name), width=qkv_size[2], height=qkv_size[0], depth=qkv_size[1], opacity=0.45, caption="Skip", fill='\\ConcatColor', bandfill='\\ConcatColor'),
        to_skip_v2(of=skip, to=kv_name, pos=1.12),
        to_ConvRes(name=k_name, s_filer=s_filer, n_filer=n_filer, offset="(0.8,0.45,0)", to="({}-east)".format(kv_name), width=qkv_size[2], height=qkv_size[0], depth=qkv_size[1], opacity=0.45, caption="K", fill='\\KColor', bandfill='\\KColor'),
        to_ConvRes(name=v_name, s_filer=s_filer, n_filer=n_filer, offset="(0.8,-0.45,0)", to="({}-east)".format(kv_name), width=qkv_size[2], height=qkv_size[0], depth=qkv_size[1], opacity=0.45, caption="V", fill='\\VColor', bandfill='\\VColor'),
        to_connection_anchor(kv_name, k_name, src_anchor="northeast", dst_anchor="west"),
        to_connection_anchor(kv_name, v_name, src_anchor="southeast", dst_anchor="west"),
        to_cross_attention(name=xca_name, s_filer=s_filer, n_filer=n_filer, offset="(1.25,0,0)", to="({}-east)".format(up_name), width=size[2], height=size[0], depth=size[1], opacity=0.6, caption="Cross-Attn"),
        # Routed orthogonal arrows keep Q/K/V paths ordered and readable.
        to_connection_orthogonal(q_name, xca_name, src_anchor="south", dst_anchor="northwest", x_step=0.45),
        to_connection_orthogonal(k_name, xca_name, src_anchor="north", dst_anchor="southwest", x_step=0.75),
        to_connection_orthogonal(v_name, xca_name, src_anchor="north", dst_anchor="southeast", x_step=1.05),
        # Residual fusion from upsampled decoder feature + cross-attn output.
        to_Sum(name=add_name, offset="(0.9,0,0)", to="({}-east)".format(xca_name), radius=1.8, opacity=0.6),
        to_connection(xca_name, add_name),
        to_connection_orthogonal(up_name, add_name, src_anchor="east", dst_anchor="south", x_step=0.55),
        to_ConvConvRelu(name=top, s_filer=s_filer, n_filer=(n_filer, n_filer), offset="(0.9,0,0)", to="({}-east)".format(add_name), width=(size[2], size[2]), height=size[0], depth=size[1], caption="Dec"),
        to_connection(add_name, top),
    ]



