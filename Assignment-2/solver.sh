#!/usr/bin/env bash

echo "Processing $1"
python2 Sudoku-CNF-generator/sudokusolver.py "$1"
picosat output.cnf -v -o result.txt
