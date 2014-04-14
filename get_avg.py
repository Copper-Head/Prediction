import sys

def main(argv):
	ppl_file = open(argv[0])
	prob = []
	for line in ppl_file.readlines():
		prob += [float(line.split(" ")[3])]
	expected_count = 0
	unexpected_count = 0
	expected_diff = 0
	unexpected_diff = 0
	for i in range(0, len(prob), 2):
		if prob[i] >= prob[i+1]:
			expected_count += 1
			expected_diff += prob[i] - prob[i+1] 
		else:
			unexpected_count += 1
			unexpected_diff += prob[i+1] - prob[i] 
	print "Expected count = " + str(expected_count)
	print "Unexpected count = " + str(unexpected_count)
	print "Expected diff avg = " + str(expected_diff/expected_count)
	print "Unexpected diff avg = " + str(unexpected_diff/unexpected_count)

if __name__ == "__main__":
	main(sys.argv[1:])
