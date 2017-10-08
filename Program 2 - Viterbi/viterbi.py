#!/usr/bin/env python

# Skylar Shyu
# CS 5340 | FL 2017
# 9/24/2017
# Programming Assignment #2
# Viterbi

import sys
import math

def _openAndStandardizeContents(fileName):
   with open(fileName, "r") as Corpus:
	Lines = Corpus.readlines()
   Corpus.close()
   return [x.lower().strip() for x in Lines]


def verifyArguments():
   argumentsOK = True 

   if (len(sys.argv) != 3):
	print "Please double check your arguments. Ensure that you have a probabilities file and a sentence file"
        argumentsOK = False

   if (str(sys.argv[1]).endswith(".txt") == False):
	print ("The first argument is not a text file (.txt). Please ensure that it is a text file.")
	argumentsOK = False

   if (str(sys.argv[2]).endswith('.txt') == False):
	print ("The second argument is not a text file (.txt). Please ensure that it is a text file.")
	argumentsOK = False

   return argumentsOK


def printOutput(sentence, probDict):
   posTags = ['noun','verb','inf','prep']
   print("PROCESSING SENTENCE: " + sentence + "\n")
   print("FINAL VITERBI NETWORK")
   processed = viterbi(sentence, probDict, posTags)
   print("\nFINAL BACKPTR NETWORK")
   backptr(processed[2], processed[1], posTags)
   #print("\n")
   seqID(processed, posTags)
   print("\n")
   
def generateProbDict(lines):
   dictionary = {str : float}
   for line in lines:
	if (line != ""):
		separated = line.split()
		key = (separated[0], separated[1])
		value = separated[2]
		dictionary[key] = float(value)
   return dictionary

def viterbi(sentence, probDict, posTags):
   separated = sentence.split()
   wordCount = len(separated)
   
   scoreTable = [[0 for x in range(wordCount)]  for i in range(4)]
   backptrTable = [[0 for x in range(wordCount)]  for i in range(4)]
   
   ## Init Step
   for i in range(0, 4):
	wordKVP = (separated[0], posTags[i]) #WORD IS WORD
	tagKVP = (posTags[i], 'phi') #WORD IS TAG

	if wordKVP in probDict:
		if tagKVP in probDict:
			scoreTable[i][0] = probDict[wordKVP] * probDict[tagKVP]
		else:
			scoreTable[i][0] = probDict[wordKVP] * 0.0001
	else:
		if tagKVP in probDict:
			scoreTable[i][0] = probDict[tagKVP] * 0.0001
		else:
			scoreTable[i][0] = 0.0001 * 0.0001
		
        backptrTable[i][0] = 0
	result = str(round(math.log(scoreTable[i][0], 2), 4))
	print("P(" + separated[0] + "=" + posTags[i] + ") = " + result)
   
   ## Iter Step
   prev = 0
   for j in range(1, wordCount):
	for i in range(0, 4):
	
		tagTagValues = []
		for k in range(0, 4):
			tag2KVP = (posTags[i], posTags[k])
			if tag2KVP in probDict:
				val = scoreTable[k][j-1] * probDict[tag2KVP]
			else:
				val = scoreTable[k][j-1] * 0.0001
			tagTagValues.append(val)
		
		if (len(tagTagValues) != 0):
			maxVal = max(tagTagValues)
		else:
			maxVal = 0		
		
		wordKVP = (separated[j], posTags[i]) #WORD IS WORD
		if wordKVP in probDict:
			scoreTable[i][j] = probDict[wordKVP] * maxVal
		else:
			scoreTable[i][j] = 0.0001 * maxVal

		backptrTable[i][j] = tagTagValues.index(max(tagTagValues))

		result = str(round(math.log(scoreTable[i][j], 2), 4))
		print("P(" + separated[j] + "=" + posTags[i] + ") = " + result)
   
   return (scoreTable, backptrTable, separated)

def backptr(separated, table, posTags):
	for j in range(1, len(separated)):
		for i in range (0, 4):
			print("Backptr(" + separated[j] + "=" + posTags[i] + ") = " + posTags[table[i][j]])


def seqID(processed, posTags):
   scoreTable = processed[0]
   backptrTable = processed[1]
   separated = processed[2]
   wordCount = len(separated)

   sequence = [0] * wordCount
   biggest = []
   
   pos = 0
   
   for i in range(0, 4):
	value = math.log(scoreTable[i][wordCount - 1], 2)
	biggest.append(value)
       
   maxVal = max(biggest)
   result = round(maxVal, 4)
   pos = biggest.index(maxVal)

   print("\nBEST TAG HAS LOG PROBABILITY = " + str(result))

   print(separated[wordCount - 1] + " -> " + str(posTags[pos]))
   if (len(separated) > 2):
	   for j in range(wordCount - 2, -1, -1):
		#print(str(j))
		print(separated[j] + " -> " + str(posTags[backptrTable[sequence[j+1]][j+1]]))
		sequence[j] = backptrTable[sequence[j+1]][j+1]
   
   if (len(separated) == 2):
	print(separated[0] + " -> " + posTags[sequence[0]])

   

def main():
   
   if (verifyArguments() == False):
	sys.exit()
   
   ## Set-up
   probsFile = sys.argv[1]
   sentsFile = sys.argv[2]

   probLines = _openAndStandardizeContents(probsFile)
   sentsLines = _openAndStandardizeContents(sentsFile)
  
   probLookup = generateProbDict(probLines)

   ## Begin analyzing sents file 
   for sentence in sentsLines:
	if (sentence != ""):
		printOutput(sentence, probLookup)

if __name__== "__main__":
  main()


