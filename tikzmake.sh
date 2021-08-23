#!/bin/bash


var1=$1
var2=${var1%%.*}

python3 ${var2}.py 
pdflatex ${var2}.tex

rm *.aux *.log *.vscodeLog
rm *.tex

if [[ "$OSTYPE" == "darwin"* ]]; then
    open ${var2}.pdf
else
    xdg-open ${var2}.pdf
fi
