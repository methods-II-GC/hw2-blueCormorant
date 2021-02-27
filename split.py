#!/usr/bin/env python3
"""Split tag file into development, training, and testing sets"""

import argparse
import random
import logging as log
from typing import Iterator, List




def read_tags(path: str) -> Iterator[List[List[str]]]:
	with open(path, "r") as source:
		lines = []
		for line in source:
			line = line.rstrip()
			if line:  # Line is contentful.
				lines.append(line.split())
			else:  # Line is blank.
				yield lines.copy()
				lines.clear()

	# Just in case someone forgets to put a blank line at the end...
	if lines:
		yield lines

def generateRand(max: int):
	num = random.randint(1, max)
	assert(num > 0 and num < max + 1)
	return num

def shuffleSets(dev: list, train: list, test: list):
	random.shuffle(dev)
	random.shuffle(train)
	random.shuffle(test)

def generateSets(inputPath: str):
	dev = []
	train = []
	test = []

	tags = read_tags(inputPath)
	for tag in tags:
		# Allocate tags to output files
		num = generateRand(10)
		if num == 1:
			dev.append(tag)
		elif num == 2:
			test.append(tag)
		else:
			train.append(tag)

	shuffleSets(dev, train, test)

	return dev, train, test

def writeFile(path: str, tags: list):
	sentenceCount = 0
	wordCount = 0
	with open(path, "w") as _file:
		for sentence in tags:
			sentenceCount = sentenceCount + 1
			for word in sentence:
				wordCount = wordCount + 1
				_file.write(' '.join(word) + "\n")

	return sentenceCount, wordCount

def seedRandomGenerator(seed: int):
	random.seed(seed)

def genTabs(count: int):
	width = 10 # Cell width
	return ''.join([' ' for elem in range(width-len(str(count)))])


def writePretty(dev: list, train: list, test: list):
	log.info("----------Sentences-----Words----")
	sCount, wCount = writeFile(args.dev, dev)
	log.info(f"| Dev   | {sCount}{genTabs(sCount)}| {wCount}{genTabs(wCount)}|")
	sCount, wCount = writeFile(args.train, train)
	log.info(f"| Train | {sCount}{genTabs(sCount)}| {wCount}{genTabs(wCount)}|")
	sCount, wCount = writeFile(args.test, test)
	log.info(f"| Test  | {sCount}{genTabs(sCount)}| {wCount}{genTabs(wCount)}|")
	log.info("---------------------------------")

def main(args: argparse.Namespace) -> None:
	seedRandomGenerator(args.seed)
	dev, train, test = generateSets(args.input)
	if args.verbose:
		writePretty(dev, train, test)
	

if __name__ == "__main__":
	
	log.basicConfig(filename='stats.log', level=log.INFO,
						format='%(levelname)s:%(message)s')	
	parser = argparse.ArgumentParser(description='Split Data for Statistical Training')
	parser.add_argument('-s', '--seed', type=int, help='Seed value', required=True)
	parser.add_argument('-v', '--verbose', help='Log statistics', action='store_true')
	parser.add_argument('input', type=str, help='Input file path')
	parser.add_argument('train', type=str, help='Training file path')
	parser.add_argument('dev', type=str, help='Development file path')
	parser.add_argument('test', type=str, help='Test file path')
	args = parser.parse_args()
	main(args)
