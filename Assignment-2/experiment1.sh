#!/usr/bin/env sh

while read p; do
  echo $p > input
  python3 main.py MODEL1 PROP_ON SPLIT_1 input | grep '^c'
done < experiment1/testCases.txt
