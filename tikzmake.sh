#!/bin/bash


python $1.py 
pdflatex $1.tex

rm *.aux *.log *.vscodeLog
rm *.tex

if [[ "$OSTYPE" == "darwin"* ]]; then
    open $1.pdf
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open $1.pdf
else
    start $1.pdf
fi
