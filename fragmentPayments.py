#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import random
#import sys


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
                      help='days from now until the end',
                      dest='daysToTheEnd'
                      )

myArgs = myParser.parse_args()
#print(myArgs)
print('amount to split=',myArgs.amountToSplit)
print('days to the end=',myArgs.daysToTheEnd)


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
def splitAmountOfCash(amountToSplit, numberOfSplits):
    INTEGER_RATIO = 100
    numberToSplit = amountToSplit * INTEGER_RATIO		# so that we play with integers
    minimumValuePerSplit = round(numberToSplit / 20)	# just trying...
    #print("minimumValuePerSplit =", minimumValuePerSplit)

    # don't go further so far
    #sys.exit(42)

    remaining = numberToSplit - minimumValuePerSplit * numberOfSplits
    #print("remaining =", remaining)

    listOfRandomNumbers = sorted([random.randint(0, remaining+1) for i in range(numberOfSplits)])
    #print(listOfRandomNumbers)

    listOfRandomNumbers.append(remaining+1)
    # "remaining+1" because otherwise, there is the risk that listOfRandomNumbers ends on :
    # ..., remaining+1, remaining ]
    # then, on the final stage (which computes x_n - x_(n-1) for number of that list) :
    # remaining - (remaining+1) = -1
    # then, when we finally add 'minimumValuePerSplit'
    # this gives a number that is less than 'minimumValuePerSplit'
    listOfRandomNumbers[0] = 1
    #print(listOfRandomNumbers)

    #print(listOfRandomNumbers[0:numberOfSplits], listOfRandomNumbers[1:numberOfSplits+1])
    # liste 1 : [0, 2, 5]
    # liste 2 : [2, 5, 5]

    return [ (j-i+minimumValuePerSplit) / INTEGER_RATIO for(i,j) in zip(listOfRandomNumbers[0:numberOfSplits], listOfRandomNumbers[1:numberOfSplits+1])]


# TODO: make a function to generate a random sequence
def splitDays(daysToSplit, numberOfSplits):
    INITIAL_WAIT_DAYS = 12	# TODO: randomize this
    MINIMUM_INTERVAL_DAYS = 2

    daysRemainingToSplit = daysToSplit - INITIAL_WAIT_DAYS - (numberOfSplits * MINIMUM_INTERVAL_DAYS)
    print("daysRemainingToSplit =",daysRemainingToSplit)

    listOfRandomNumbers = sorted([random.randint(0, daysRemainingToSplit+1) for i in range(numberOfSplits)])
    print("listOfRandomNumbers (generated) : ",listOfRandomNumbers)

    listOfRandomNumbers.append(daysRemainingToSplit + 1)
    listOfRandomNumbers[0] = 1
    print("listOfRandomNumbers (first,last) : ",listOfRandomNumbers)

    print ( [ j-i+MINIMUM_INTERVAL_DAYS for(i,j) in zip(listOfRandomNumbers[0:numberOfSplits], listOfRandomNumbers[1:numberOfSplits+1])] )



def slice(totalLength, numberOfSlices, fixedFirstSliceLength, minimumSliceLength, ratio=1):

    totalLength = totalLength * ratio
    fixedFirstSliceLength = fixedFirstSliceLength * ratio
    minimumSliceLength = minimumSliceLength * ratio

    if (fixedFirstSliceLength != 0):
        numberOfSlices = numberOfSlices - 1

    lengthToSlice = totalLength - fixedFirstSliceLength - (numberOfSlices * minimumSliceLength)
#    print("minimumSliceLength", minimumSliceLength)
#    print("lengthToSlice = ",lengthToSlice)
    listOfRandomNumbers = sorted([random.randint(0, round(lengthToSlice + 1)) for i in range(numberOfSlices)])
    listOfRandomNumbers.append(lengthToSlice + 1)
    listOfRandomNumbers[0] = 1
    result = [ (j-i+minimumSliceLength)/ratio for(i,j) in zip(listOfRandomNumbers[0:numberOfSlices], listOfRandomNumbers[1:numberOfSlices+1])]

    if (fixedFirstSliceLength != 0):
        result.insert(0, fixedFirstSliceLength/ratio)

    return result




numberOfSplits = 7
splitted = splitAmountOfCash(myArgs.amountToSplit, numberOfSplits)
print(splitted, "\t", sum(splitted), "\t", myArgs.amountToSplit-sum(splitted))



cash=slice( totalLength           = myArgs.amountToSplit,
            numberOfSlices        = numberOfSplits,
            fixedFirstSliceLength = 0,
            minimumSliceLength    = round(myArgs.amountToSplit/20),
            ratio                 = 100
            )

print(cash, "\t", sum(cash), "\t", myArgs.amountToSplit-sum(cash))



#splitDays(myArgs.daysToTheEnd, numberOfSplits)
