
def read_stats(filename):
	f = open(filename, 'r')
	a = [line for line in f if line[0] == "c" or line[0] == "s"]
	#decision = []
	#run_time = []
	stats = []
	for i in a:
		if "decision" in i:
			decision_number = filter(str.isdigit, i)
			#print decision_number
			#decision.append(decision_number)
		if "total run time" in i:
			run_time_number = filter(str.isdigit, i)
			#print run_time_number
			#run_time.append(run_time_number)
		statscollection = filter(str.isdigit, i)
		stats.append(statscollection)

	print stats	
	return decision_number , run_time_number 	