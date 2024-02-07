#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import random
import sys


myParser = argparse.ArgumentParser(description='This script does things with numbers')
myParser.add_argument(
                    '--amount',
                    metavar='A',
                    type=float,
                    default=123.45,
                    help='the amount to split',
                    dest='amountToSplit'
                    )
myParser.add_argument(
                    '--days',
                    metavar='D',
                    type=int,
                    default=42,
                    help='days from now until the last payment is made',
                    dest='daysToLastPayment'
                    )

myArgs = myParser.parse_args()
print(myArgs)
print('amount to split=',myArgs.amountToSplit)
print('days to last payment=',myArgs.daysToLastPayment)


# The method to split any number N into n numbers that sum to N is to :
# - consider a book having N pages
# - place n-1 bookmarks randomly inside the book
# - the n random numbers are the number of pages of each segment
#
# If you add the extra constraint that all splits must be > x :
# - subtract (n*x) from the book length
# - share the remaining
# - then add x to eeach section
#
# source : https://stackoverflow.com/a/50604179/2312935


numberToSplit = myArgs.amountToSplit * 100	# so that we play with integers
minimumValuePerSplit = numberToSplit / 10	# just trying...
numberOfSplits = 7

remaining = numberToSplit - minimumValuePerSplit * numberOfSplits
print("remaining =", remaining)

# don't go further so far
sys.exit(42)

listOfRandomNumbers = sorted([random.randint(0, remaining+1) for i in range(numberOfSplits)])
print(listOfRandomNumbers)

#listOfRandomNumbers.append(remaining)
#listOfRandomNumbers[0] = 0

listOfRandomNumbers.append(remaining+1)
# "remaining+1" because otherwise, there is the risk that listOfRandomNumbers ends on :
# ..., remaining+1, remaining ]
# then, on the final stage (which computes x_n - x_(n-1) for number of that list) :
# remaining - (remaining+1) = -1
# then, when we finally add 'minimumValuePerSplit'
# this gives a number that is less than 'minimumValuePerSplit'
listOfRandomNumbers[0] = 1
print(listOfRandomNumbers)

#print(listOfRandomNumbers[0:numberOfSplits], listOfRandomNumbers[1:numberOfSplits+1])
# liste 1 : [0, 2, 5]
# liste 2 : [2, 5, 5]

result = [j-i+minimumValuePerSplit for(i,j) in zip(listOfRandomNumbers[0:numberOfSplits], listOfRandomNumbers[1:numberOfSplits+1])]
print(numberToSplit, result, sum(result))
