#!/usr/bin/env python3

import numpy as np
import copy
fullSudoku = open('testFull.txt', 'r')
board = next(fullSudoku)
for i in range(1, 72, 3):
    for m in range(200):
        boardC = [board[k] for k in range(len(board) - 1)]
        indexes = np.arange(len(board) - 1)
        np.random.shuffle(indexes)
        for j in range(i):
            boardC[indexes[j]] = '.'
        print(''.join(boardC))
