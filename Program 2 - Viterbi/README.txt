# Skylar Shyu
# CS 5340 | FL 2017
# 9/24/2017
# Programming Assignment #2
# Viterbi - README.TXT

a) Python 2.7. was used.

b) No compilation is necessary to run the code. To run, type the following in a terminal:
				./viterbi.py <probabilities_file> <sentences_file>
   An example:	./viterbi.py probs.txt sents.txt
   It is important to ensure that both files are .txt format and in the order specified above!

c) The code was tested on CADE lab machine lab1-18. 

d) No known bugs or errors. However, the two if-statements in method seqID() are very much work around
   and I'm pretty sure they're not robust if a sentence only happens to contain 'one' word. 
