#!/bin/bash


python $1.py 
pdflatex $1.tex

rm -f *.aux *.log *.out *.fls *.fdb_latexmk *.vscodeLog
rm -f *.tex

if [[ "$OSTYPE" == "darwin"* ]]; then
    open $1.pdf
else
    xdg-open $1.pdf
fi
