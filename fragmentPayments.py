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
def slice(totalLength, numberOfSlices, fixedFirstSliceLength, minimumSliceLength, ratio=1):

    # the slicing below works with integers. Multiplying everything by 100 changes amounts of cash (floats) into "integers".
    totalLength = totalLength * ratio
    fixedFirstSliceLength = fixedFirstSliceLength * ratio
    minimumSliceLength = minimumSliceLength * ratio

    if (fixedFirstSliceLength != 0):
        numberOfSlices = numberOfSlices - 1

    lengthToSlice = totalLength - fixedFirstSliceLength - (numberOfSlices * minimumSliceLength)
    listOfRandomNumbers = sorted([random.randint(0, round(lengthToSlice + 1)) for i in range(numberOfSlices)])
    listOfRandomNumbers.append(lengthToSlice + 1)
    # "lengthToSlice+1" because otherwise, there is the risk that listOfRandomNumbers ends on :
    # ..., lengthToSlice+1, lengthToSlice ]
    # then, on the final stage (which computes x_n - x_(n-1) for number of that list) :
    # lengthToSlice - (lengthToSlice+1) = -1
    # then, when we finally add 'minimumValuePerSplit'
    # this gives a number that is less than 'minimumValuePerSplit'

    listOfRandomNumbers[0] = 1
    result = [ (j-i+minimumSliceLength)/ratio for(i,j) in zip(listOfRandomNumbers[0:numberOfSlices], listOfRandomNumbers[1:numberOfSlices+1])]

    if (fixedFirstSliceLength != 0):
        result.insert(0, fixedFirstSliceLength/ratio)

    return result




numberOfSplits = 3


cash=slice( totalLength           = myArgs.amountToSplit,
            numberOfSlices        = numberOfSplits,
            fixedFirstSliceLength = 0,
            minimumSliceLength    = round(myArgs.amountToSplit/20),	# so that I have a decent minimum amount
            ratio                 = 100
            )
print(cash, "\t", sum(cash), "\t", myArgs.amountToSplit - sum(cash))


# TODO: check that
# - 'fixedFirstSliceLength' < amount to split
# - numberOfSlices * minimumSliceLength < amount to split
delays=slice(totalLength          = myArgs.daysToTheEnd,
            numberOfSlices        = numberOfSplits,
            fixedFirstSliceLength = 2,
            minimumSliceLength    = 2,
            )
print(delays, "\t", sum(delays), "\t", myArgs.daysToTheEnd - sum(delays))




import datetime

today = datetime.datetime.now().astimezone()
todayPlusNDays= today + datetime.timedelta(days=27)
#print(today.strftime('%Y-%m-%d'))
#print(todayPlusNDays.strftime('%Y-%m-%d'))

listOfPayDays=[today]
for i in range(numberOfSplits):
    listOfPayDays.append(listOfPayDays[i] + datetime.timedelta(days=delays[i]))

print([ truc.strftime('%Y-%m-%d') for truc in listOfPayDays ])


# TODO: display summary as a list :
# on the <date>, pay <slice of cash>
