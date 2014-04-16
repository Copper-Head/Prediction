import sys
from argparse import ArgumentParser
import re

# IK:
# below import needed for some csv writing functionality 
# disabled, since the "gum" module is something I wrote and not part of a 
# vanilla python installation
# from gum import *


def write_out(out_name, data_dict):
	output_template = '{0} = {1}'
	with open(out_name, 'w') as out_file:
		# print data_dict
		for key, value in data_dict.items():
			out_file.write(output_template.format(key, value) + '\n')


def mod_f_name(f_name):
	return f_name.split('.')[0] + '.stats'


def expected_unexpected(probs):	
	to_return = {}
	to_return['Expected count'] = sum(1 for i in range(0, len(probs), 2)
			if probs[i] >= probs[i+1])
	to_return['Unexpected count'] = len(probs) - to_return['Expected count']
	expected_diff = sum(probs[i] - probs[i+1] 
		for i in range(0, len(probs), 2)
		if probs[i] >= probs[i+1])
	to_return['Expected Diff avg'] = expected_diff / to_return['Expected count']
	unexpected_diff = sum(probs[i+1] - probs[i] 
		for i in range(0, len(probs), 2)
		if probs[i] < probs[i+1])
	to_return['Unexpected Diff avg'] = unexpected_diff / to_return['Unexpected count']
	return to_return


def overall_avg(probs):
	to_return = {}
	to_return['count when plausible has greater prob'] = sum(1 for i in range(0, len(probs), 2)
			if probs[i] >= probs[i+1])
	diff_sum = sum(probs[i] - probs[i+1] for i in range(0, len(probs), 2))
	to_return['avg difference between s1 and s2'] = diff_sum / to_return['count when plausible has greater prob']
	return to_return


def process_file(f_name):
	with open(f_name) as ppl_file:
		probs = [float(line.split()[3]) for line in ppl_file.readlines()]
		# return expected_unexpected(probs)
		return overall_avg(probs)


def make_row_dict(prob_cond):
	return {'probability': prob_cond[0],
	'condition': prob_cond[1]
	}


def read_ppl(f_name):
	with open(f_name) as ppl_file:
		return (float(line.split()[3]) for line in ppl_file.readlines())


def combine_prob_condition(ppl_file, stim_file):
	stims = list(unprocessed_csv(stim_file))
	probs = list(read_ppl(ppl_file))
	assert len(stims) == len(probs), 'problem!'
	stims_condcode = (r['condcode'] for r in stims)
	return [make_row_dict(pair) for pair in zip(probs, stims_condcode)]
	

def main():
	''' Here we set up any functionality necessary for whatever we're doing.
	'''
	parser = ArgumentParser()
	# this is functionality for collecting some stats from ppl files
	parser.add_argument('files', nargs='+')
	file_list = parser.parse_args().files
	for f_name in file_list:		
		write_out(mod_f_name(f_name), process_file(f_name))
	# stuff for generating pairings of ppls and condition codes
	# parser.add_argument('expname')
	# parser.add_argument('stims')
	# parser.add_argument('ppl')
	# args = parser.parse_args()
	# header = ['probability', 'condition']
	# data = combine_prob_condition(args.ppl, args.stims)
	# out_name = args.expname + '_paired.csv'
	# write_to_csv(out_name, data, header)


if __name__ == "__main__":
	main()
