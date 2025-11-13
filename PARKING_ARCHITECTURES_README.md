# PlotNeuralNet for Parking Occupancy Prediction Models

This guide shows how to create **publication-quality 3D neural network architecture diagrams** for your 13 deep learning models using PlotNeuralNet.

## 🎨 Why Use PlotNeuralNet?

**Before (matplotlib):** Simple boxes and arrows
**After (PlotNeuralNet):** Professional 3D visualizations like in top papers!

### Benefits:
- ✅ **Publication-ready** vector PDFs (scalable to any size)
- ✅ **3D perspective** shows layer depth and connections clearly
- ✅ **Professional appearance** for papers, presentations, thesis
- ✅ **Consistent styling** across all architectures
- ✅ **Skip connections** for ResNet/U-Net style architectures

---

## 📦 Quick Start

### 1. Navigate to examples directory
```bash
cd pyexamples/
```

### 2. Generate a single architecture
```bash
# Generate DNN architecture
python parking_dl_architectures.py dnn

# This creates: 01_DNN_Architecture.tex
```

### 3. Compile to PDF
```bash
# Use the provided build script
bash ../tikzmake.sh 01_DNN_Architecture

# Or compile manually
pdflatex 01_DNN_Architecture.tex
```

### 4. View the PDF
The PDF will open automatically, or open manually:
```bash
# Linux
xdg-open 01_DNN_Architecture.pdf

# macOS
open 01_DNN_Architecture.pdf

# Windows
start 01_DNN_Architecture.pdf
```

---

## 🚀 Generate All 13 Architectures

### Generate all at once:
```bash
python parking_dl_architectures.py all
```

Then compile each one:
```bash
for file in *_Architecture.tex; do
    pdflatex "$file"
done
```

### Or use a script:
```bash
# Create compile_all.sh
cat > compile_all.sh << 'EOF'
#!/bin/bash
models="dnn lstm gru bilstm cnn cnn_lstm cnn_gru convlstm tcn transformer attention_lstm encoder_decoder wavenet"
for model in $models; do
    echo "Compiling $model..."
    python parking_dl_architectures.py $model
    pdflatex ${model}_Architecture.tex
    rm *.aux *.log 2>/dev/null
done
EOF

chmod +x compile_all.sh
./compile_all.sh
```

---

## 📋 Available Models

| Command | Model Name | Architecture Type |
|---------|-----------|-------------------|
| `dnn` | Deep Neural Network | Feedforward |
| `lstm` | Long Short-Term Memory | Recurrent |
| `gru` | Gated Recurrent Unit | Recurrent |
| `bilstm` | Bidirectional LSTM | Bidirectional |
| `cnn` | Convolutional Neural Network | Convolutional |
| `cnn_lstm` | CNN-LSTM Hybrid | Hybrid |
| `cnn_gru` | CNN-GRU Hybrid | Hybrid |
| `convlstm` | Convolutional LSTM | Spatial-Temporal |
| `tcn` | Temporal Convolutional Network | Dilated Conv |
| `transformer` | Transformer | Self-Attention |
| `attention_lstm` | Attention-LSTM | Attention |
| `encoder_decoder` | Encoder-Decoder | Seq2Seq |
| `wavenet` | WaveNet | Dilated Residual |

---

## 🎯 Customization Guide

### Layer Type Mappings

PlotNeuralNet provides these layer types:

| Your Layer | PlotNeuralNet Function | Visual Appearance |
|------------|----------------------|-------------------|
| Dense/FC | `to_Conv()` | Solid colored box |
| LSTM/GRU | `to_ConvConvRelu()` | Banded box (shows gates) |
| Dropout | `to_Pool()` with opacity | Transparent box |
| Conv1D/2D | `to_Conv()` | Blue box |
| Pooling | `to_Pool()` | Red semi-transparent |
| Attention | `to_Conv()` + custom color | Yellow/orange box |
| Activation | Part of layer caption | Text in caption |
| Concatenate | `to_Conv()` | Wide box |
| Sum/Add | `to_Sum()` | Sphere with + symbol |

### Color Scheme

Edit colors in `pycore/tikzeng.py:14-23`:
```latex
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}      % Convolution
\def\PoolColor{rgb:red,1;black,0.3}               % Pooling
\def\SoftmaxColor{rgb:magenta,5;black,7}          % Output
\def\SumColor{rgb:blue,5;green,15}                % Operations
```

### Layer Parameters

**Size parameters control visual appearance:**
```python
to_Conv(
    name="layer1",           # Unique identifier
    s_filer=256,             # Feature map size (label on z-axis)
    n_filer=64,              # Number of filters (label on x-axis)
    offset="(2,0,0)",        # Position offset (x,y,z)
    to="(prev_layer-east)",  # Anchor to previous layer
    height=40,               # Visual height (y dimension)
    depth=40,                # Visual depth (z dimension)
    width=2,                 # Visual width (x dimension, represents filters)
    caption="Conv(64)\\\\ReLU"  # Label below layer
)
```

**Tips:**
- `height` and `depth`: Make similar for square feature maps
- `width`: Increase for more channels/filters (thicker box)
- Use `\\\\` for line breaks in captions
- Offset controls spacing between layers

---

## 🔧 Advanced Customization

### 1. Add Skip Connections (ResNet, U-Net style)

```python
# Layer definitions
to_Conv("layer1", ...),
to_Conv("layer2", ...),
to_Conv("layer3", ...),

# Add skip connection from layer1 to layer3
to_skip(of="layer1", to="layer3", pos=1.25),
```

### 2. Bidirectional Layers (BiLSTM)

```python
# Forward path (offset upward)
to_ConvConvRelu("lstm_fwd", offset="(2,2,0)", ...),

# Backward path (offset downward)
to_ConvConvRelu("lstm_bwd", offset="(2,-2,0)", ...),

# Concatenate
to_Conv("concat", ...),
to_connection("lstm_fwd", "concat"),
to_connection("lstm_bwd", "concat"),
```

### 3. Add Input Images

```python
# Add sample input image
to_input('../path/to/image.jpg', to='(-3,0,0)', width=4, height=4, name="input"),
```

### 4. Multi-Head Attention (Transformer)

```python
# Multiple attention heads side by side
for i in range(4):
    x_offset = 2 + i * 1.5
    to_Conv(f"head_{i}", offset=f"({x_offset},0,0)",
            width=1, height=30, depth=30, caption=f"Head {i}")
```

### 5. Custom Layer Colors

Define new colors in your architecture:
```python
arch = [
    to_head('..'),

    # Add custom color definitions
    r"""\def\CustomColor{rgb:blue,3;green,5;white,2}""",

    to_cor(),
    to_begin(),

    # Use custom color
    r"""\pic[shift={(0,0,0)}] at (0,0,0)
        {Box={
            name=custom,
            fill=\CustomColor,
            height=40, width=2, depth=40
        }
    };""",

    # ... rest of architecture
]
```

---

## 📊 Example Modifications

### Increase Layer Sizes for Better Visibility

**Original:**
```python
to_Conv("dense1", s_filer=256, n_filer=256, height=40, depth=40, width=3)
```

**Larger:**
```python
to_Conv("dense1", s_filer=256, n_filer=256, height=60, depth=60, width=5)
```

### Add More Spacing Between Layers

**Original:**
```python
to_Conv("layer2", offset="(2,0,0)", to="(layer1-east)")
```

**More space:**
```python
to_Conv("layer2", offset="(4,0,0)", to="(layer1-east)")
```

### Change Caption Style

```python
# Multi-line caption
caption="LSTM(128)\\\\return\_seq=True\\\\dropout=0.2"

# Math notation
caption="Dense(256)\\\\$\\sigma(Wx+b)$"

# Bold
caption="\\textbf{Output Layer}"
```

---

## 🎨 Creating Custom Architectures

### Template Structure

```python
def create_custom_architecture():
    arch = [
        # 1. Document setup
        to_head('..'),
        to_cor(),
        to_begin(),

        # 2. Input layer
        to_Conv("input", s_filer=X, n_filer=Y,
                offset="(0,0,0)", to="(0,0,0)",
                height=H, depth=D, width=W,
                caption="Input\\\\T×F"),

        # 3. Hidden layers
        to_Conv("layer1", ...),
        to_connection("input", "layer1"),

        to_Conv("layer2", ...),
        to_connection("layer1", "layer2"),

        # 4. Output layer
        to_SoftMax("output", 7, offset="(2,0,0)",
                   to="(layerN-east)",
                   caption="Output(7)"),
        to_connection("layerN", "output"),

        # 5. Close document
        to_end()
    ]
    return arch
```

---

## 🐛 Troubleshooting

### Error: "Command not found: pdflatex"

**Solution:** Install LaTeX:
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-extra texlive-fonts-recommended

# macOS
brew install --cask mactex

# Windows
# Download and install MikTeX from https://miktex.org/
```

### Error: "File not found: init.tex"

**Solution:** Make sure you're in the `pyexamples/` directory:
```bash
cd /path/to/PlotNeuralNet/pyexamples/
```

### Layers overlap or look wrong

**Solution:** Adjust spacing:
```python
# Increase offset between layers
offset="(3,0,0)"  # instead of (2,0,0)

# Or adjust layer sizes
height=30  # instead of 40
```

### Skip connections don't show properly

**Solution:** Adjust the `pos` parameter:
```python
to_skip(of="layer1", to="layer3", pos=1.25)  # Try 1.0, 1.5, 2.0
```

### PDF won't open automatically

**Manually open:**
```bash
ls -la *.pdf  # Find your PDF
xdg-open your_architecture.pdf  # Linux
open your_architecture.pdf      # macOS
```

---

## 📐 Size Guidelines for Different Paper Sizes

### For A4 Paper / Standard Papers
```python
height=40, depth=40, width=2-3  # Standard layers
height=60, depth=60, width=4-5  # Important/large layers
```

### For Posters / Presentations
```python
height=80, depth=80, width=6-8  # Larger for visibility
```

### For Two-Column Papers
```python
height=30, depth=30, width=2  # Compact
offset="(1.5,0,0)"             # Tighter spacing
```

---

## 💡 Tips for Best Results

1. **Consistent sizing:** Keep similar layers the same size
2. **Logical flow:** Left to right, input to output
3. **Clear labels:** Use descriptive captions with layer parameters
4. **Color coding:** Use different colors for different layer types
5. **White space:** Don't overcrowd - use appropriate offsets
6. **Legend:** Add text annotations for special features
7. **Compile often:** Check PDF after each major change

---

## 📚 Layer Function Reference

### Basic Layers

**to_Conv()** - Convolutional / Dense layers
```python
to_Conv(name, s_filer, n_filer, offset, to, height, depth, width, caption)
```

**to_ConvConvRelu()** - Multi-operation layers (LSTM/GRU)
```python
to_ConvConvRelu(name, s_filer, n_filer=(64,64), offset, to,
                width=(3,3), height, depth, caption)
```

**to_Pool()** - Pooling / Dropout layers
```python
to_Pool(name, offset, to, height, depth, width, opacity, caption)
```

**to_SoftMax()** - Output layers
```python
to_SoftMax(name, s_filer, offset, to, width, height, depth, caption)
```

**to_Sum()** - Element-wise operations
```python
to_Sum(name, offset, to, radius, opacity)
```

### Connection Functions

**to_connection()** - Regular arrows
```python
to_connection("from_layer", "to_layer")
```

**to_skip()** - Skip connections (curved)
```python
to_skip(of="source", to="target", pos=1.25)
```

---

## 🎓 Learning Resources

1. **PlotNeuralNet Documentation:** See `README.md` in main directory
2. **Example Architectures:** Check `examples/` folder for CNN, U-Net, etc.
3. **TikZ Documentation:** https://tikz.dev/ for advanced LaTeX graphics
4. **Paper Examples:**
   - U-Net paper: https://arxiv.org/abs/1505.04597
   - FCN paper: https://arxiv.org/abs/1411.4038

---

## 🤝 Contributing

Found a better way to represent a layer? Improved the code?
- Fork the repository
- Make your changes
- Submit a pull request

---

## 📜 License

This code extends PlotNeuralNet (MIT License) for parking occupancy prediction models.

---

## ✨ Quick Reference Card

```bash
# Generate architecture
python parking_dl_architectures.py lstm

# Compile to PDF
bash ../tikzmake.sh 02_LSTM_Architecture

# Generate all
python parking_dl_architectures.py all

# Common layer sizes
height=40, depth=40, width=2    # Small
height=50, depth=50, width=3    # Medium
height=60, depth=60, width=4    # Large

# Spacing
offset="(1.5,0,0)"  # Tight
offset="(2,0,0)"    # Normal
offset="(3,0,0)"    # Wide
```

---

**Happy Visualizing! 🎨**

For questions or issues, check the main PlotNeuralNet documentation or open an issue on GitHub.
