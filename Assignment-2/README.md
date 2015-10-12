# CSP Solver
Constraint satisfaction problem solver for Sudoku boards

Run:
```
python3 main.py {MODEL1|MODEL2} {PROP_ON|PROP_OFF} {SPLIT_1,SPLIT_2} test2.txt
```

MODEL1 - Fills cells by numbers

MODEL2 - Fills numbers by cells 
FOR MODEL 2 not all test work

IF YOU WANT TO CHECK IF model TAKE FILES OUT OF EXPERIMENTS1 

PROP_ON - With propagation heuristic

PROP_OFF - Without propagation heuristic
PROP_OFF takes a long time to compute!!!!!!

SPLIT_1 - Naive splitting

SPLIT_2 - Pick a variable with less domain first
