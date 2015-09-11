#!/usr/bin/env bash

python2 Sudoku-CNF-generator/sudokusolver.py $1
picosat output.cnf -v
