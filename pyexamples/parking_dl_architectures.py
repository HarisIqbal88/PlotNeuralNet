"""
Visualize Deep Learning Architectures for Multi-Horizon Parking Occupancy Prediction
Using PlotNeuralNet for Publication-Quality 3D Diagrams
=====================================================================================

This script generates professional 3D architecture diagrams for all 13 DL models:
1. DNN (Deep Neural Network)
2. LSTM (Long Short-Term Memory)
3. GRU (Gated Recurrent Unit)
4. BiLSTM (Bidirectional LSTM)
5. CNN (Convolutional Neural Network)
6. CNN-LSTM (Hybrid)
7. CNN-GRU (Hybrid)
8. ConvLSTM (Convolutional LSTM)
9. TCN (Temporal Convolutional Network)
10. Transformer (Self-Attention)
11. Attention-LSTM
12. Encoder-Decoder
13. WaveNet

Author: PlotNeuralNet Adaptation
Date: November 2025

Usage:
    python parking_dl_architectures.py dnn        # Generate DNN architecture
    python parking_dl_architectures.py lstm       # Generate LSTM architecture
    python parking_dl_architectures.py all        # Generate all architectures
"""

import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *


# ============================================================================
# 1. DNN (Deep Neural Network)
# ============================================================================
def create_dnn_architecture():
    """
    DNN: Input -> Dense(256) -> Dropout -> Dense(128) -> Dropout -> Dense(64) -> Output(7)
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_input('../examples/fcn8s/cats.jpg', to='(-3,0,0)', width=4, height=4, name="input"),

        # Input representation
        to_Conv("input_layer", s_filer=37, n_filer=36, offset="(1,0,0)", to="(input-east)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),
        to_connection("input", "input_layer"),

        # Dense layer 1 (256 units)
        to_Conv("dense1", s_filer=256, n_filer=256, offset="(2,0,0)", to="(input_layer-east)",
                height=50, depth=50, width=4, caption="Dense(256)\\\\ReLU"),
        to_connection("input_layer", "dense1"),

        # Dropout 1
        to_Pool("dropout1", offset="(0,0,0)", to="(dense1-east)",
                height=50, depth=50, width=1, opacity=0.3, caption="Dropout(0.3)"),

        # Dense layer 2 (128 units)
        to_Conv("dense2", s_filer=128, n_filer=128, offset="(2,0,0)", to="(dropout1-east)",
                height=40, depth=40, width=3, caption="Dense(128)\\\\ReLU"),
        to_connection("dropout1", "dense2"),

        # Dropout 2
        to_Pool("dropout2", offset="(0,0,0)", to="(dense2-east)",
                height=40, depth=40, width=1, opacity=0.3, caption="Dropout(0.3)"),

        # Dense layer 3 (64 units)
        to_Conv("dense3", s_filer=64, n_filer=64, offset="(2,0,0)", to="(dropout2-east)",
                height=30, depth=30, width=2, caption="Dense(64)\\\\ReLU"),
        to_connection("dropout2", "dense3"),

        # Output layer (7 horizons)
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense3-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense3", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 2. LSTM Architecture
# ============================================================================
def create_lstm_architecture():
    """
    LSTM: Input -> LSTM(128) -> Dense(64) -> Dropout -> Dense(32) -> Output(7)
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # LSTM layer (128 units) - represented as banded box
        to_ConvConvRelu("lstm1", s_filer=128, n_filer=(128,128), offset="(2,0,0)",
                        to="(input-east)", width=(5,5), height=45, depth=45,
                        caption="LSTM(128)\\\\return\_seq=True"),
        to_connection("input", "lstm1"),

        # Dense layer 1 (64 units)
        to_Conv("dense1", s_filer=64, n_filer=64, offset="(2.5,0,0)", to="(lstm1-east)",
                height=35, depth=35, width=2, caption="Dense(64)\\\\ReLU"),
        to_connection("lstm1", "dense1"),

        # Dropout
        to_Pool("dropout", offset="(0,0,0)", to="(dense1-east)",
                height=35, depth=35, width=1, opacity=0.3, caption="Dropout(0.2)"),

        # Dense layer 2 (32 units)
        to_Conv("dense2", s_filer=32, n_filer=32, offset="(2,0,0)", to="(dropout-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("dropout", "dense2"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense2-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense2", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 3. GRU Architecture
# ============================================================================
def create_gru_architecture():
    """
    GRU: Input -> GRU(128) -> Dense(64) -> Dropout -> Dense(32) -> Output(7)
    Similar to LSTM but with different internal gates (uses pink/magenta color)
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # GRU layer (128 units) - use different color scheme
        to_ConvConvRelu("gru1", s_filer=128, n_filer=(128,128), offset="(2,0,0)",
                        to="(input-east)", width=(4.5,4.5), height=45, depth=45,
                        caption="GRU(128)\\\\return\_seq=True"),
        to_connection("input", "gru1"),

        # Dense layer 1 (64 units)
        to_Conv("dense1", s_filer=64, n_filer=64, offset="(2.5,0,0)", to="(gru1-east)",
                height=35, depth=35, width=2, caption="Dense(64)\\\\ReLU"),
        to_connection("gru1", "dense1"),

        # Dropout
        to_Pool("dropout", offset="(0,0,0)", to="(dense1-east)",
                height=35, depth=35, width=1, opacity=0.3, caption="Dropout(0.2)"),

        # Dense layer 2 (32 units)
        to_Conv("dense2", s_filer=32, n_filer=32, offset="(2,0,0)", to="(dropout-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("dropout", "dense2"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense2-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense2", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 4. BiLSTM Architecture
# ============================================================================
def create_bilstm_architecture():
    """
    BiLSTM: Input -> BiLSTM(64×2) -> Concatenate -> Dense(32) -> Output(7)
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # Forward LSTM (represented above)
        to_ConvConvRelu("lstm_fwd", s_filer=64, n_filer=(64,64), offset="(2,2,0)",
                        to="(input-east)", width=(3,3), height=35, depth=35,
                        caption="Forward\\\\LSTM(64)"),
        to_connection("input", "lstm_fwd"),

        # Backward LSTM (represented below)
        to_ConvConvRelu("lstm_bwd", s_filer=64, n_filer=(64,64), offset="(2,-2,0)",
                        to="(input-east)", width=(3,3), height=35, depth=35,
                        caption="Backward\\\\LSTM(64)"),
        to_connection("input", "lstm_bwd"),

        # Concatenate layer
        to_Conv("concat", s_filer=128, n_filer=128, offset="(3,0,0)", to="(lstm_fwd-east)",
                height=40, depth=40, width=3, caption="Concatenate\\\\128 units"),
        to_connection("lstm_fwd", "concat"),
        to_connection("lstm_bwd", "concat"),

        # Dropout
        to_Pool("dropout", offset="(0,0,0)", to="(concat-east)",
                height=40, depth=40, width=1, opacity=0.3, caption="Dropout(0.2)"),

        # Dense layer (32 units)
        to_Conv("dense", s_filer=32, n_filer=32, offset="(2,0,0)", to="(dropout-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("dropout", "dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 5. CNN Architecture
# ============================================================================
def create_cnn_architecture():
    """
    CNN: Input -> Conv1D(64) -> MaxPool -> Conv1D(128) -> GlobalAvgPool -> Dense -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # Conv1D layer 1 (64 filters)
        to_Conv("conv1", s_filer=64, n_filer=34, offset="(2,0,0)", to="(input-east)",
                height=38, depth=38, width=3, caption="Conv1D(64)\\\\kernel=3"),
        to_connection("input", "conv1"),

        # MaxPooling1D
        to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)",
                height=19, depth=19, width=3, opacity=0.5, caption="MaxPool1D\\\\size=2"),

        # Conv1D layer 2 (128 filters)
        to_Conv("conv2", s_filer=128, n_filer=17, offset="(2,0,0)", to="(pool1-east)",
                height=16, depth=16, width=4, caption="Conv1D(128)\\\\kernel=3"),
        to_connection("pool1", "conv2"),

        # GlobalAveragePooling1D
        to_Pool("gap", offset="(0,0,0)", to="(conv2-east)",
                height=10, depth=10, width=4, opacity=0.5, caption="GlobalAvgPool"),

        # Dense layer (64 units)
        to_Conv("dense", s_filer=64, n_filer=64, offset="(2,0,0)", to="(gap-east)",
                height=30, depth=30, width=2, caption="Dense(64)\\\\ReLU"),
        to_connection("gap", "dense"),

        # Dropout
        to_Pool("dropout", offset="(0,0,0)", to="(dense-east)",
                height=30, depth=30, width=1, opacity=0.3, caption="Dropout(0.3)"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dropout-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dropout", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 6. CNN-LSTM Hybrid Architecture
# ============================================================================
def create_cnn_lstm_architecture():
    """
    CNN-LSTM: Input -> Conv1D -> MaxPool -> LSTM -> Dense -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # Conv1D layer (64 filters)
        to_Conv("conv1", s_filer=64, n_filer=34, offset="(2,0,0)", to="(input-east)",
                height=38, depth=38, width=3, caption="Conv1D(64)\\\\kernel=3"),
        to_connection("input", "conv1"),

        # MaxPooling1D
        to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)",
                height=19, depth=19, width=3, opacity=0.5, caption="MaxPool1D"),

        # LSTM layer (64 units)
        to_ConvConvRelu("lstm", s_filer=64, n_filer=(64,64), offset="(2.5,0,0)",
                        to="(pool1-east)", width=(4,4), height=35, depth=35,
                        caption="LSTM(64)"),
        to_connection("pool1", "lstm"),

        # Dropout
        to_Pool("dropout", offset="(0,0,0)", to="(lstm-east)",
                height=35, depth=35, width=1, opacity=0.3, caption="Dropout(0.3)"),

        # Dense layer (32 units)
        to_Conv("dense", s_filer=32, n_filer=32, offset="(2,0,0)", to="(dropout-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("dropout", "dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 7. CNN-GRU Hybrid Architecture
# ============================================================================
def create_cnn_gru_architecture():
    """
    CNN-GRU: Input -> Conv1D -> MaxPool -> GRU -> Dense -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # Conv1D layer (64 filters)
        to_Conv("conv1", s_filer=64, n_filer=34, offset="(2,0,0)", to="(input-east)",
                height=38, depth=38, width=3, caption="Conv1D(64)\\\\kernel=3"),
        to_connection("input", "conv1"),

        # MaxPooling1D
        to_Pool("pool1", offset="(0,0,0)", to="(conv1-east)",
                height=19, depth=19, width=3, opacity=0.5, caption="MaxPool1D"),

        # GRU layer (64 units)
        to_ConvConvRelu("gru", s_filer=64, n_filer=(64,64), offset="(2.5,0,0)",
                        to="(pool1-east)", width=(3.5,3.5), height=35, depth=35,
                        caption="GRU(64)"),
        to_connection("pool1", "gru"),

        # Dropout
        to_Pool("dropout", offset="(0,0,0)", to="(gru-east)",
                height=35, depth=35, width=1, opacity=0.3, caption="Dropout(0.3)"),

        # Dense layer (32 units)
        to_Conv("dense", s_filer=32, n_filer=32, offset="(2,0,0)", to="(dropout-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("dropout", "dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 8. TCN (Temporal Convolutional Network) Architecture
# ============================================================================
def create_tcn_architecture():
    """
    TCN: Input -> Dilated Conv (d=1) -> Dilated Conv (d=2) -> Dilated Conv (d=4) -> GAP -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # Dilated Conv layer 1 (dilation=1)
        to_Conv("dconv1", s_filer=64, n_filer=36, offset="(2,0,0)", to="(input-east)",
                height=40, depth=40, width=2.5, caption="DilatedConv\\\\d=1, k=3"),
        to_connection("input", "dconv1"),

        # Dilated Conv layer 2 (dilation=2)
        to_Conv("dconv2", s_filer=64, n_filer=36, offset="(2,0,0)", to="(dconv1-east)",
                height=40, depth=40, width=2.5, caption="DilatedConv\\\\d=2, k=3"),
        to_connection("dconv1", "dconv2"),

        # Dilated Conv layer 3 (dilation=4)
        to_Conv("dconv3", s_filer=64, n_filer=36, offset="(2,0,0)", to="(dconv2-east)",
                height=40, depth=40, width=2.5, caption="DilatedConv\\\\d=4, k=3"),
        to_connection("dconv2", "dconv3"),

        # GlobalAveragePooling
        to_Pool("gap", offset="(0,0,0)", to="(dconv3-east)",
                height=12, depth=12, width=2.5, opacity=0.5, caption="GlobalAvgPool"),

        # Dense layer (32 units)
        to_Conv("dense", s_filer=32, n_filer=32, offset="(2,0,0)", to="(gap-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("gap", "dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 9. Transformer Architecture
# ============================================================================
def create_transformer_architecture():
    """
    Transformer: Input -> Embedding -> Multi-Head Attention -> FFN -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # Embedding + Positional Encoding
        to_Conv("embed", s_filer=128, n_filer=36, offset="(2,0,0)", to="(input-east)",
                height=40, depth=40, width=3, caption="Embedding\\\\+PosEnc"),
        to_connection("input", "embed"),

        # Multi-Head Attention (represented as special layer)
        to_ConvConvRelu("mha", s_filer=128, n_filer=(128,128), offset="(2.5,0,0)",
                        to="(embed-east)", width=(5,5), height=45, depth=45,
                        caption="Multi-Head\\\\Attention"),
        to_connection("embed", "mha"),

        # Add & Norm
        to_Sum("add1", offset="(1,0,0)", to="(mha-east)", radius=2, opacity=0.6),
        to_connection("mha", "add1"),

        # Feed-Forward Network
        to_Conv("ffn", s_filer=128, n_filer=128, offset="(2,0,0)", to="(add1-east)",
                height=45, depth=45, width=3, caption="FFN\\\\Dense"),
        to_connection("add1", "ffn"),

        # Add & Norm
        to_Sum("add2", offset="(1,0,0)", to="(ffn-east)", radius=2, opacity=0.6),
        to_connection("ffn", "add2"),

        # Global Average Pooling
        to_Pool("gap", offset="(1.5,0,0)", to="(add2-east)",
                height=15, depth=15, width=2, opacity=0.5, caption="GAP"),
        to_connection("add2", "gap"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(gap-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("gap", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 10. Attention-LSTM Architecture
# ============================================================================
def create_attention_lstm_architecture():
    """
    Attention-LSTM: Input -> LSTM (encoder) -> Attention -> Context -> Dense -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # LSTM Encoder (return sequences)
        to_ConvConvRelu("lstm_enc", s_filer=128, n_filer=(128,36), offset="(2,0,0)",
                        to="(input-east)", width=(5,5), height=45, depth=45,
                        caption="LSTM\\\\Encoder(128)"),
        to_connection("input", "lstm_enc"),

        # Attention mechanism (represented as special colored layer)
        to_Conv("attention", s_filer=128, n_filer=36, offset="(2.5,0,0)", to="(lstm_enc-east)",
                height=40, depth=40, width=4, caption="Attention\\\\Mechanism"),
        to_connection("lstm_enc", "attention"),

        # Context vector (weighted sum)
        to_Sum("context", offset="(1.5,0,0)", to="(attention-east)", radius=2.5, opacity=0.6),
        to_connection("attention", "context"),

        # Dense layer
        to_Conv("dense", s_filer=64, n_filer=64, offset="(2,0,0)", to="(context-east)",
                height=30, depth=30, width=2, caption="Dense(64)\\\\ReLU"),
        to_connection("context", "dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 11. Encoder-Decoder Architecture
# ============================================================================
def create_encoder_decoder_architecture():
    """
    Encoder-Decoder: Input -> LSTM Encoder -> RepeatVector -> LSTM Decoder -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # LSTM Encoder
        to_ConvConvRelu("encoder", s_filer=128, n_filer=(128,128), offset="(2,0,0)",
                        to="(input-east)", width=(5,5), height=45, depth=45,
                        caption="LSTM\\\\Encoder(128)"),
        to_connection("input", "encoder"),

        # Bottleneck / Context vector
        to_Conv("bottleneck", s_filer=128, n_filer=1, offset="(2,0,0)", to="(encoder-east)",
                height=25, depth=25, width=3, caption="Context\\\\Vector"),
        to_connection("encoder", "bottleneck"),

        # RepeatVector (7 times for 7 horizons)
        to_Conv("repeat", s_filer=128, n_filer=7, offset="(2,0,0)", to="(bottleneck-east)",
                height=20, depth=20, width=3, caption="RepeatVec\\\\(7)"),
        to_connection("bottleneck", "repeat"),

        # LSTM Decoder
        to_ConvConvRelu("decoder", s_filer=64, n_filer=(64,7), offset="(2.5,0,0)",
                        to="(repeat-east)", width=(4,4), height=30, depth=30,
                        caption="LSTM\\\\Decoder(64)"),
        to_connection("repeat", "decoder"),

        # TimeDistributed Dense
        to_Conv("td_dense", s_filer=7, n_filer=7, offset="(2,0,0)", to="(decoder-east)",
                height=20, depth=20, width=2, caption="TimeDistrib\\\\Dense"),
        to_connection("decoder", "td_dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(td_dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("td_dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 12. WaveNet Architecture
# ============================================================================
def create_wavenet_architecture():
    """
    WaveNet: Input -> Causal Conv blocks with residual connections -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\36×37"),

        # Causal Conv Block 1 (dilation=1)
        to_ConvRes("res1", s_filer=64, n_filer=36, offset="(2,0,0)", to="(input-east)",
                   width=3, height=40, depth=40, opacity=0.5, caption="Causal\\\\d=1"),
        to_connection("input", "res1"),

        # Causal Conv Block 2 (dilation=2)
        to_ConvRes("res2", s_filer=64, n_filer=36, offset="(2,0,0)", to="(res1-east)",
                   width=3, height=40, depth=40, opacity=0.5, caption="Causal\\\\d=2"),
        to_connection("res1", "res2"),
        to_skip(of="res1", to="res2", pos=1.25),

        # Causal Conv Block 3 (dilation=4)
        to_ConvRes("res3", s_filer=64, n_filer=36, offset="(2,0,0)", to="(res2-east)",
                   width=3, height=40, depth=40, opacity=0.5, caption="Causal\\\\d=4"),
        to_connection("res2", "res3"),
        to_skip(of="res2", to="res3", pos=1.25),

        # GlobalAveragePooling
        to_Pool("gap", offset="(1,0,0)", to="(res3-east)",
                height=15, depth=15, width=2, opacity=0.5, caption="GAP"),
        to_connection("res3", "gap"),

        # Dense layer
        to_Conv("dense", s_filer=32, n_filer=32, offset="(2,0,0)", to="(gap-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("gap", "dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# 13. ConvLSTM Architecture
# ============================================================================
def create_convlstm_architecture():
    """
    ConvLSTM: Input -> ConvLSTM2D layers -> Flatten -> Dense -> Output
    """
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),

        # Input layer (reshaped for ConvLSTM)
        to_Conv("input", s_filer=37, n_filer=36, offset="(0,0,0)", to="(0,0,0)",
                height=40, depth=40, width=1, caption="Input\\\\(36,1,37,1)"),

        # ConvLSTM2D layer 1 (64 filters)
        to_ConvConvRelu("convlstm1", s_filer=64, n_filer=(64,36), offset="(2,0,0)",
                        to="(input-east)", width=(5,5), height=42, depth=42,
                        caption="ConvLSTM2D\\\\(64)"),
        to_connection("input", "convlstm1"),

        # ConvLSTM2D layer 2 (32 filters)
        to_ConvConvRelu("convlstm2", s_filer=32, n_filer=(32,36), offset="(2.5,0,0)",
                        to="(convlstm1-east)", width=(4,4), height=38, depth=38,
                        caption="ConvLSTM2D\\\\(32)"),
        to_connection("convlstm1", "convlstm2"),

        # Flatten
        to_Pool("flatten", offset="(1,0,0)", to="(convlstm2-east)",
                height=25, depth=25, width=2, opacity=0.5, caption="Flatten"),
        to_connection("convlstm2", "flatten"),

        # Dense layer
        to_Conv("dense", s_filer=32, n_filer=32, offset="(2,0,0)", to="(flatten-east)",
                height=25, depth=25, width=1.5, caption="Dense(32)\\\\ReLU"),
        to_connection("flatten", "dense"),

        # Output layer
        to_SoftMax("output", 7, offset="(2,0,0)", to="(dense-east)",
                   width=1.5, height=3, depth=20, caption="Output(7)\\\\Sigmoid"),
        to_connection("dense", "output"),

        to_end()
    ]
    return arch


# ============================================================================
# Main execution
# ============================================================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python parking_dl_architectures.py <model_name>")
        print("\nAvailable models:")
        print("  dnn, lstm, gru, bilstm, cnn, cnn_lstm, cnn_gru,")
        print("  convlstm, tcn, transformer, attention_lstm,")
        print("  encoder_decoder, wavenet, all")
        sys.exit(1)

    model = sys.argv[1].lower()

    architectures = {
        'dnn': ('01_DNN', create_dnn_architecture),
        'lstm': ('02_LSTM', create_lstm_architecture),
        'gru': ('03_GRU', create_gru_architecture),
        'bilstm': ('04_BiLSTM', create_bilstm_architecture),
        'cnn': ('05_CNN', create_cnn_architecture),
        'cnn_lstm': ('06_CNN_LSTM', create_cnn_lstm_architecture),
        'cnn_gru': ('07_CNN_GRU', create_cnn_gru_architecture),
        'convlstm': ('08_ConvLSTM', create_convlstm_architecture),
        'tcn': ('09_TCN', create_tcn_architecture),
        'transformer': ('10_Transformer', create_transformer_architecture),
        'attention_lstm': ('11_Attention_LSTM', create_attention_lstm_architecture),
        'encoder_decoder': ('12_Encoder_Decoder', create_encoder_decoder_architecture),
        'wavenet': ('13_WaveNet', create_wavenet_architecture)
    }

    if model == 'all':
        print("Generating all 13 architectures...")
        for name, (prefix, func) in architectures.items():
            filename = f'{prefix}_Architecture'
            arch = func()
            to_generate(arch, filename + '.tex')
            print(f"✓ Generated {filename}.tex")
    elif model in architectures:
        prefix, func = architectures[model]
        filename = f'{prefix}_Architecture'
        arch = func()
        to_generate(arch, filename + '.tex')
        print(f"✓ Generated {filename}.tex")
        print(f"\nTo compile:")
        print(f"  pdflatex {filename}.tex")
        print(f"Or use: bash ../tikzmake.sh {filename}")
    else:
        print(f"Unknown model: {model}")
        print("Use one of: " + ", ".join(architectures.keys()) + ", all")
        sys.exit(1)


if __name__ == '__main__':
    main()
