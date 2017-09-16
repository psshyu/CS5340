#!/usr/bin/env python

# Skylar Shyu
# CS 5340 | FL 2017
# 9/10/2017
# Programming Assignment #1
# N-grams

import sys
import math

def _openAndStandardizeContents(fileName):
   with open(fileName, "r") as Corpus:
	Lines = Corpus.readlines()
   Corpus.close()
   return [x.lower().strip() for x in Lines]


def _bigramStripSentence(sentence):
   splittedSentence = filter(lambda x: x != '', sentence.split(" "))
   splittedSentence.insert(0, "^")
   return splittedSentence

def unigramProb(trainingUnigrams, sentence):
   splittedSentence = filter(lambda x: x != '', sentence.split(" "))
   result = 0
   totalFrequency = sum(trainingUnigrams.values())

   for word in splittedSentence:
	wordFrequency = trainingUnigrams.get(word)
	if (trainingUnigrams.has_key(str(word)) == True):  
		result += math.log(wordFrequency/float(totalFrequency), 2)
	else:
		return "undefined"

   return round(result, 4)

def bigramProb(trainingBigramUnigrams, trainingBigrams, bigrams, sentence):
   splittedSentence = _bigramStripSentence(sentence)
   result = 0
   
   for i in range(0, len(splittedSentence) - 1):
	
	if (trainingBigrams.has_key(tuple([splittedSentence[i], splittedSentence[i+1]])) == True and trainingBigramUnigrams.has_key(splittedSentence[i])):
		wordFrequency = trainingBigrams.get(tuple([splittedSentence[i], splittedSentence[i+1]]))
		totalFrequency = trainingBigramUnigrams.get(splittedSentence[i])
		result += math.log(wordFrequency/float(totalFrequency), 2)
	else:
		return "undefined"

   return round(result, 4)

def bigramProbAddOne(trainingBigramUnigrams, trainingBigrams, bigrams, sentence):
   splittedSentence = _bigramStripSentence(sentence)
   result = 0
   uniqueUnigrams = len(trainingBigramUnigrams)

   for i in range(0, len(splittedSentence) - 1):

	wordFrequency = trainingBigrams.get(tuple([splittedSentence[i], splittedSentence[i+1]]), 0) + 1
	totalFrequency = trainingBigramUnigrams.get(splittedSentence[i]) + uniqueUnigrams
	result += math.log(wordFrequency/float(totalFrequency), 2)

   return round(result, 4)

def verifyArguments():
   argumentsOK = True 

   if (len(sys.argv) != 4):
	print "Please double check your arguments. Ensure that you have a training file, the test flag, and a testing file"
        argumentsOK = False

   if (str(sys.argv[1]).endswith(".txt") == False):
	print ("The first argument is not a text file (.txt). Please ensure that it is a text file.")
	argumentsOK = False
   
   if (sys.argv[2] != "-test"):
	print ("The flag " + sys.argv[2] + " is not a valid flag. Please use -test to run this script.")
	argumentsOK = False

   if (str(sys.argv[3]).endswith('.txt') == False):
	print ("The third argument is not a text file (.txt). Please ensure that it is a text file.")
	argumentsOK = False

   return argumentsOK

def printOutput(trainingUnigrams, trainingBigramUnigrams, trainingBigrams, bigrams, sentence):
   print("S = " + sentence + "\n")
   print("\n")
   print("Unsmoothed Unigrams, logprob(S) = " + str(unigramProb(trainingUnigrams, sentence)) + "\n")
   print("Unsmoothed Bigrams, logprob(S) = " + str(bigramProb(trainingBigramUnigrams, trainingBigrams, bigrams, sentence)) + "\n")
   print("Smoothed Bigrams, logprob(S) = " + str(bigramProbAddOne(trainingBigramUnigrams, trainingBigrams, bigrams, sentence)) + "\n")
   print("\n")

def main():
   
   if (verifyArguments() == False):
	sys.exit()
   
   ## Set-up
   trainingFile = sys.argv[1]
   testFile = sys.argv[3]

   trainingUnigrams = {}
   trainingBigramUnigrams = {"^" : 0}
   trainingBigrams = {}

   bigramPile = []

   lines = _openAndStandardizeContents(trainingFile)
   
   ## Begin unigram processing
   for line in lines:
	if (line != ""):
		separated = line.split()
		for word in separated:
		     if(trainingUnigrams.has_key(word) == True):
			trainingUnigrams[str(word)] = trainingUnigrams.get(str(word)) + 1
		     else:
			trainingUnigrams[word] = 1

   ## Begin bigram processing
   for sentence in lines:
	
	if (sentence != ""):
		separated = sentence.split()
		bigramPile.append("^")
		trainingBigramUnigrams["^"] = trainingBigramUnigrams.get("^") + 1
		for i in range(len(separated)):
		     if(trainingBigramUnigrams.has_key(separated[i]) == True):
			trainingBigramUnigrams[str(separated[i])] = trainingBigramUnigrams.get(str(separated[i])) + 1
		     else:
			trainingBigramUnigrams[separated[i]] = 1
   		     bigramPile.append(separated[i])
   
   bigrams = zip(bigramPile, bigramPile[1:])
   bigrams = filter(lambda x : x[1].endswith("^") is False, bigrams)
   
   for pair in bigrams:
	if (trainingBigrams.has_key(pair) == True):
		trainingBigrams[pair] = trainingBigrams.get(pair) + 1
	else:
		trainingBigrams[pair] = 1
   
   ## Begin analyzing test file and print results
   testLines = _openAndStandardizeContents(testFile)

   for sentence in testLines:
	if (sentence != ""):
		printOutput(trainingUnigrams, trainingBigramUnigrams, trainingBigrams, bigrams, sentence)

if __name__== "__main__":
  main()


