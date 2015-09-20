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
        if "c conflicts" in i:
            print(">>>>", i.split(':')[1].split()[0])
            conflicts_number = float(i.split(':')[1].split()[0])
        elif "conflicts\n" in i:
            conflicts_number = float(i.split(' ')[1])
        elif "c decisions" in i:
            decisions_number = float(i.split(':')[1].split()[0])
        elif "decisions\n" in i:
            decisions_number = float(i.split(' ')[1])
        elif "fixed variables\n" in i:
            fixed_variables = float(i.split(' ')[1])
        elif "learned literals\n" in i:
            learned_literals = float(i.split(' ')[1])
        elif "deleted literals\n" in i:
            deleted_literals = float(i.split(' ')[1][:-1])
        elif "propagations\n" in i:
            propogations = float(i.split(' ')[1])
        elif "visits\n" in i:
            visits_number = float(i.split(' ')[1])
            print('Visits:', visits_number)
            #decision.append(decision_number)
        elif "variables used\n" in i:
            variables_used = float(i.split(' ')[1][:-1])
        elif "total run time" in i:
            run_time_number = float(i.split(' ')[1])
            print('Runtime:', run_time_number)
            #run_time.append(run_time_number)
        #statscollection = list(filter(str.isdigit, i))
        #stats.append(statscollection)

    #print(stats)
    return [conflicts_number, decisions_number]
    #return [conflicts_number, decisions_number, fixed_variables, learned_literals, deleted_literals, propogations, visits_number, variables_used, run_time_number]

levels = ['Super easy',
          'Very easy',
          'Easy',
          'Medium',
          'Hard',
          'Harder',
          'Very hard',
          'Super hard',
          'Impossible']

results = []
for idx, level in enumerate(levels):
    for f in os.listdir(level):
        subprocess.call(['./solver2.sh "%s/%s"' % (level, f)], shell=True)
        results.append([idx] + read_stats('result.txt'))
        print(results[-1])

import numpy as np
results = np.array(results)
np.save('experiment_results_cryptominisat.npy', results)
