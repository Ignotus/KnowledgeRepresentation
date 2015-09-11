import os
import subprocess

def read_stats(filename):
    f = open(filename, 'r')
    a = [line for line in f if line[0] == "c" or line[0] == "s"]
    print(a)
    #decision = []
    #run_time = []
    #stats = []
    for i in a:
        if "visits\n" in i:
            visits_number = float(i.split(' ')[1])
            print('Visits:', visits_number)
            #decision.append(decision_number)
        elif "total run time" in i:
            run_time_number = float(i.split(' ')[1])
            print('Runtime:', run_time_number)
            #run_time.append(run_time_number)
        #statscollection = list(filter(str.isdigit, i))
        #stats.append(statscollection)

    #print(stats)
    return [visits_number , run_time_number]

levels = ['Super easy',
          'Very easy',
          'Easy',
          'Medium',
          'Hard',
          'Harder',
          'Very hard',
          'Super hard']

results = []
for idx, level in enumerate(levels):
    for f in os.listdir(level):
        subprocess.call(['./solver.sh "%s/%s"' % (level, f)], shell=True)
        results.append([idx] + read_stats('result.txt'))

import numpy as np
results = np.array(results)
np.save('experiment_results.npy', results)
