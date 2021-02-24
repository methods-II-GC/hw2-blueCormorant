#!/usr/bin/env python3
"""One-line description of the program goes here."""

import argparse
import random
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
	with open(path, "w") as _file:
		for sentence in tags:
			for word in sentence:
				_file.write(' '.join(word) + "\n")

def main(args: argparse.Namespace) -> None:
	#corpus = list(read_tags("conll2000.txt"))
	dev, train, test = generateSets(args.input)
	#print(len(dev), len(train), len(test))
	writeFile(args.dev, dev)
	writeFile(args.train, train)
	writeFile(args.test, test)

if __name__ == "__main__":
	# TODO: declare arguments.
	# TODO: parse arguments and pass them to `main`.
	# main()
	parser = argparse.ArgumentParser(description='Split Data for Statistical Training')
	parser.add_argument('input', type=str, help='Input file path')
	parser.add_argument('train', type=str, help='Training file path')
	parser.add_argument('dev', type=str, help='Development file path')
	parser.add_argument('test', type=str, help='Test file path')
	args = parser.parse_args()
	main(args)
