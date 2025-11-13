#!/bin/bash
#
# Build All Parking Prediction Architecture Diagrams
# ==================================================
# This script generates and compiles all 13 DL architecture diagrams
#

echo "=========================================="
echo "Building All Architecture Diagrams"
echo "=========================================="
echo ""

# Create output directory
mkdir -p parking_architectures_output

# List of all models
models=(
    "dnn:01_DNN"
    "lstm:02_LSTM"
    "gru:03_GRU"
    "bilstm:04_BiLSTM"
    "cnn:05_CNN"
    "cnn_lstm:06_CNN_LSTM"
    "cnn_gru:07_CNN_GRU"
    "convlstm:08_ConvLSTM"
    "tcn:09_TCN"
    "transformer:10_Transformer"
    "attention_lstm:11_Attention_LSTM"
    "encoder_decoder:12_Encoder_Decoder"
    "wavenet:13_WaveNet"
)

success_count=0
fail_count=0

# Process each model
for model_info in "${models[@]}"; do
    IFS=':' read -r model prefix <<< "$model_info"
    filename="${prefix}_Architecture"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Processing: $model ($filename)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Generate LaTeX
    echo "  [1/3] Generating LaTeX..."
    if python parking_dl_architectures.py "$model"; then
        echo "  ✓ LaTeX generated"
    else
        echo "  ✗ Failed to generate LaTeX"
        ((fail_count++))
        continue
    fi

    # Compile to PDF
    echo "  [2/3] Compiling to PDF..."
    if pdflatex -interaction=nonstopmode "${filename}.tex" > /dev/null 2>&1; then
        echo "  ✓ PDF compiled"
    else
        echo "  ✗ Failed to compile PDF"
        ((fail_count++))
        continue
    fi

    # Move to output directory
    echo "  [3/3] Moving to output directory..."
    if mv "${filename}.pdf" parking_architectures_output/; then
        echo "  ✓ Moved to parking_architectures_output/"
        ((success_count++))
    else
        echo "  ✗ Failed to move PDF"
        ((fail_count++))
        continue
    fi

    echo ""
done

# Cleanup temporary files
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Cleaning up temporary files..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
rm -f *.aux *.log *.tex *.synctex.gz 2>/dev/null
echo "✓ Cleanup complete"
echo ""

# Summary
echo "=========================================="
echo "BUILD SUMMARY"
echo "=========================================="
echo "✓ Successful: $success_count"
echo "✗ Failed:     $fail_count"
echo "=========================================="
echo ""

if [ $success_count -gt 0 ]; then
    echo "📁 Output directory: parking_architectures_output/"
    echo ""
    echo "Generated PDFs:"
    ls -lh parking_architectures_output/*.pdf 2>/dev/null | awk '{print "  -", $9, "("$5")"}'
    echo ""
fi

if [ $fail_count -eq 0 ]; then
    echo "✅ All architectures built successfully!"
    echo ""
    echo "💡 To view all PDFs:"
    echo "   cd parking_architectures_output"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   open *.pdf"
    else
        echo "   xdg-open *.pdf"
    fi
else
    echo "⚠️  Some architectures failed to build."
    echo "   Check error messages above for details."
fi

echo ""
echo "=========================================="
echo "DONE"
echo "=========================================="
