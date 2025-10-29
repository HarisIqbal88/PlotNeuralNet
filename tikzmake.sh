#!/bin/bash


python $1.py 
pdflatex $1.tex

rm -rf *.aux *.log *.vscodeLog
rm -rf *.tex

if [[ "$OSTYPE" == "darwin"* ]]; then
    open $1.pdf
else
    xdg-open $1.pdf
fi
