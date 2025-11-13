# 🚀 Quick Start Guide: PlotNeuralNet for Your 13 DL Models

## ⚡ 5-Minute Start

### Step 1: Install LaTeX (One-time setup)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra
```

**macOS:**
```bash
brew install --cask mactex
# Or download from: https://www.tug.org/mactex/
```

**Windows:**
- Download MikTeX from https://miktex.org/download
- Install with default options

### Step 2: Generate Your First Architecture

```bash
cd pyexamples/

# Generate DNN architecture
python parking_dl_architectures.py dnn

# Compile to PDF
pdflatex 01_DNN_Architecture.tex

# View the result
xdg-open 01_DNN_Architecture.pdf  # Linux
# open 01_DNN_Architecture.pdf     # macOS
# start 01_DNN_Architecture.pdf    # Windows
```

### Step 3: Generate All 13 Architectures

```bash
# Use the automated build script
chmod +x build_all_architectures.sh
./build_all_architectures.sh

# All PDFs will be in: parking_architectures_output/
```

---

## 📋 Available Models

Generate any model with:
```bash
python parking_dl_architectures.py <model_name>
```

| Model Name | Command | Description |
|------------|---------|-------------|
| DNN | `dnn` | Deep Neural Network (feedforward) |
| LSTM | `lstm` | Long Short-Term Memory |
| GRU | `gru` | Gated Recurrent Unit |
| BiLSTM | `bilstm` | Bidirectional LSTM |
| CNN | `cnn` | 1D Convolutional Network |
| CNN-LSTM | `cnn_lstm` | Hybrid CNN + LSTM |
| CNN-GRU | `cnn_gru` | Hybrid CNN + GRU |
| ConvLSTM | `convlstm` | Convolutional LSTM |
| TCN | `tcn` | Temporal Convolutional Network |
| Transformer | `transformer` | Self-Attention Network |
| Attention-LSTM | `attention_lstm` | LSTM with Attention |
| Encoder-Decoder | `encoder_decoder` | Seq2Seq Network |
| WaveNet | `wavenet` | Dilated Causal Convolution |
| **All** | `all` | **Generate all 13 models** |

---

## 🎯 What You Get

### Professional 3D Visualizations:
- ✅ Publication-quality PDF outputs
- ✅ Vector graphics (scalable to any size)
- ✅ 3D isometric perspective
- ✅ Consistent styling across all models
- ✅ Perfect for papers, thesis, presentations

### Your Matplotlib Code (Old):
```python
# 50+ lines per architecture
# 2D flat boxes
# Raster PNG outputs
# Basic appearance
```

### PlotNeuralNet (New):
```python
# 30-40 lines per architecture
# 3D perspective boxes
# Vector PDF outputs
# Professional appearance
```

---

## 📂 File Structure

After running the build script:
```
PlotNeuralNet_1/
├── pyexamples/
│   ├── parking_dl_architectures.py      # Main script
│   ├── build_all_architectures.sh       # Build all script
│   └── parking_architectures_output/    # Generated PDFs
│       ├── 01_DNN_Architecture.pdf
│       ├── 02_LSTM_Architecture.pdf
│       ├── 03_GRU_Architecture.pdf
│       ├── 04_BiLSTM_Architecture.pdf
│       ├── 05_CNN_Architecture.pdf
│       ├── 06_CNN_LSTM_Architecture.pdf
│       ├── 07_CNN_GRU_Architecture.pdf
│       ├── 08_ConvLSTM_Architecture.pdf
│       ├── 09_TCN_Architecture.pdf
│       ├── 10_Transformer_Architecture.pdf
│       ├── 11_Attention_LSTM_Architecture.pdf
│       ├── 12_Encoder_Decoder_Architecture.pdf
│       └── 13_WaveNet_Architecture.pdf
├── PARKING_ARCHITECTURES_README.md      # Detailed guide
├── MATPLOTLIB_vs_PLOTNEURALNET.md       # Comparison guide
└── QUICKSTART_GUIDE.md                  # This file
```

---

## 🔧 Common Commands

### Generate Single Architecture
```bash
python parking_dl_architectures.py lstm
pdflatex 02_LSTM_Architecture.tex
```

### Generate All Architectures
```bash
./build_all_architectures.sh
```

### Clean Up Temporary Files
```bash
rm -f *.aux *.log *.tex
```

### View All PDFs
```bash
cd parking_architectures_output/
ls *.pdf
```

---

## 💡 Quick Customization

Want to adjust how an architecture looks? Edit `parking_dl_architectures.py`:

### Make Layers Bigger:
```python
# Before
height=40, depth=40, width=2

# After (larger)
height=60, depth=60, width=4
```

### Add More Spacing:
```python
# Before
offset="(2,0,0)"

# After (more space)
offset="(3,0,0)"
```

### Change Caption:
```python
# Before
caption="LSTM(128)"

# After (more detail)
caption="LSTM(128)\\\\dropout=0.2\\\\return\_seq=True"
```

---

## 🎨 Layer Visual Guide

### What Each Layer Looks Like:

**Dense/FC Layer:**
```
     ╱──────╲
    ╱ Dense  ╲
   ╱  (256)   ╲
  ╱    ReLU    ╲
 ╱──────────────╲
```
Wide box, thickness = number of units

**LSTM/GRU Layer:**
```
     ╱═══════╲
    ║║ LSTM  ║║  <- Banded (shows internal gates)
   ║║ (128)  ║║
  ║║─────────║║
 ╱═══════════╲
```
Banded box suggests internal complexity

**Conv Layer:**
```
     ╱─────╲
    ╱ Conv ╲
   ╱  (64)  ╲
  ╱─────────╲
```
Blue box, size shows feature maps

**Pooling/Dropout:**
```
     ╱────╲
    ╱▓▓▓▓▓╲  <- Semi-transparent
   ╱▓Pool▓╲
  ╱▓▓▓▓▓▓▓╲
```
Transparent red box

**Output:**
```
  ╱╲
 ╱  ╲
╱Out ╲  <- Tall thin box
╲ (7)╱
 ╲  ╱
  ╲╱
```
Magenta tall box

**Skip Connection:**
```
Layer1 ─┐
        │
Layer2  │
        │
Layer3 ←┘  <- Curved arrow
```
Curved connection between non-adjacent layers

---

## 📊 Usage Examples

### Example 1: Generate DNN for Your Paper
```bash
cd pyexamples/
python parking_dl_architectures.py dnn
pdflatex 01_DNN_Architecture.tex

# Include in LaTeX paper:
\begin{figure}[h]
  \centering
  \includegraphics[width=0.8\textwidth]{01_DNN_Architecture.pdf}
  \caption{Deep Neural Network Architecture for Multi-Horizon Prediction}
  \label{fig:dnn_arch}
\end{figure}
```

### Example 2: Generate All Models for Comparison
```bash
./build_all_architectures.sh

# Create comparison figure in your paper showing all 13
```

### Example 3: Customize LSTM Before Generating
```bash
# Edit parking_dl_architectures.py
# Find create_lstm_architecture() function
# Adjust parameters
# Then generate:
python parking_dl_architectures.py lstm
pdflatex 02_LSTM_Architecture.tex
```

---

## 🐛 Troubleshooting

### "Command not found: pdflatex"
→ Install LaTeX (see Step 1)

### "File not found: init.tex"
→ Make sure you're in `pyexamples/` directory:
```bash
cd /path/to/PlotNeuralNet_1/pyexamples/
```

### Layers look too small/large
→ Edit the `height`, `depth`, `width` parameters in the architecture function

### Need more space between layers
→ Increase `offset` parameter, e.g., `offset="(3,0,0)"`

### Want different colors
→ Edit color definitions in `pycore/tikzeng.py` lines 14-23

---

## 📚 Next Steps

1. **Read detailed guides:**
   - `PARKING_ARCHITECTURES_README.md` - Complete usage guide
   - `MATPLOTLIB_vs_PLOTNEURALNET.md` - Why switch & comparison

2. **Explore examples:**
   - Check `examples/` folder for more architectures
   - Study `AlexNet`, `Unet`, `VGG16` examples

3. **Customize your diagrams:**
   - Edit `parking_dl_architectures.py`
   - Adjust layer sizes, spacing, colors
   - Add custom annotations

4. **Use in your work:**
   - Include PDFs in your paper
   - Add to thesis chapters
   - Use in presentations

---

## ✅ Checklist

Before publishing, make sure:
- [ ] All 13 architectures generated successfully
- [ ] PDFs look good at 100% and 200% zoom
- [ ] Layer labels are clear and readable
- [ ] Consistent styling across all diagrams
- [ ] Proper spacing between layers
- [ ] Captions are informative
- [ ] Colors match your paper's color scheme

---

## 🎓 Publication Tips

### For Journal Papers:
- Use all 13 diagrams in a comparison figure
- Show detailed view of your best-performing model
- Include architecture diagram in methodology section

### For Conference Papers:
- Show 3-5 key architectures
- Focus on your novel contributions
- Use in related work for comparison

### For Thesis:
- Dedicate a section to architecture visualization
- Show all 13 models with detailed captions
- Compare with related work architectures

---

## 💬 Need Help?

1. **Check documentation:**
   - `PARKING_ARCHITECTURES_README.md` - Detailed guide
   - `MATPLOTLIB_vs_PLOTNEURALNET.md` - Comparison
   - Main `README.md` - PlotNeuralNet docs

2. **Look at examples:**
   - `examples/` folder has working examples
   - Study how they structure architectures

3. **Common issues:**
   - Most problems are LaTeX installation or path issues
   - Make sure you're in the correct directory
   - Check that all files are in place

---

## 🎉 You're Ready!

You now have:
- ✅ Complete code for all 13 architectures
- ✅ Automated build script
- ✅ Professional 3D visualizations
- ✅ Publication-quality PDFs
- ✅ Comprehensive documentation

**Start with:**
```bash
cd pyexamples/
python parking_dl_architectures.py dnn
pdflatex 01_DNN_Architecture.tex
```

**Then explore and customize!**

---

**Happy Publishing! 📊🎓✨**
