#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# For description + help + usage, read below or run "./<program_name>.py -h"

import argparse
import random
import sys
import datetime



def error(errorMessage):
    print(errorMessage)
    sys.exit(1)



# The method to split any number N into n numbers that sum to N is to :
# - consider a book having N pages
# - place n-1 bookmarks randomly inside the book
# - the n random numbers are the number of pages between 2 successive bookmarks
#   - "successive" is why "sorted" is used below
#   - considering page 1 and page N of the book, those n numbers sum to N
#
# If you add the extra constraint that all splits must be > x :
# - subtract (n*x) from the book length
# - share the remaining
# - then add x to eeach section
#
# source : https://stackoverflow.com/a/50604179/2312935
def slice(totalLength, numberOfSlices, fixedFirstSliceLength, minimumSliceLength, ratio=1):

    if(fixedFirstSliceLength >= totalLength):
        error("The fixed-value 1st split ('{}' given) must be shorter than "
              "the amount to split ('{}' given)".format(fixedFirstSliceLength, totalLength))

    if(numberOfSlices * minimumSliceLength >= totalLength):
        error("nb of splits ({}) * min. split value ({}) must be less than "
              "the amount to split ({})".format(numberOfSlices, minimumSliceLength, totalLength))

    # The slicing works with integers. Multiplying everything by a 'ratio' of 100
    # changes amounts of cash (floats) into "integers".
    totalLength_converted = totalLength * ratio
    fixedFirstSliceLength_converted = fixedFirstSliceLength * ratio
    minimumSliceLength_converted = minimumSliceLength * ratio

    if (fixedFirstSliceLength != 0):
        numberOfSlices = numberOfSlices - 1

    lengthToSlice = totalLength_converted - fixedFirstSliceLength_converted - (numberOfSlices * minimumSliceLength_converted)
    if(lengthToSlice < -1):
        error("Nothing left to split :\n"
              "\tleft to split = amount to split ({}) - fixed-value 1st split ({}) - (nb of splits ({}) * min. split value ({}))\n"
              "doesn't work. Check input values.".format(
                totalLength_converted,
                fixedFirstSliceLength_converted,
                numberOfSlices,
                minimumSliceLength_converted
                )
            )

    listOfRandomNumbers = sorted([random.randint(0, round(lengthToSlice + 1)) for i in range(numberOfSlices)])
    listOfRandomNumbers.append(lengthToSlice + 1)
    # "lengthToSlice+1" because otherwise, there is the risk that listOfRandomNumbers
    # ends on :
    #   ..., lengthToSlice+1, lengthToSlice ]
    # then, on the final stage (which computes x_n - x_(n-1) for number of that list) :
    # lengthToSlice - (lengthToSlice+1) = -1
    # then, when we finally add 'minimumValuePerSplit'
    # this gives a number that is less than 'minimumValuePerSplit'

    listOfRandomNumbers[0] = 1
    result = [ (j-i+minimumSliceLength_converted)/ratio for(i,j) in zip(listOfRandomNumbers[0:numberOfSlices], listOfRandomNumbers[1:numberOfSlices+1]) ]

    if (fixedFirstSliceLength != 0):
        result.insert(0, fixedFirstSliceLength)

    return result



myParser = argparse.ArgumentParser(
    description='''This program outputs the least convenient way of repaying a debt by computing :
    - uneven payments
    - separated by uneven delays
given :
    - the amount to pay
    - the total delay
    - the number of payments

⚠️  Under the hood, this also adds an initial delay (currently hardcoded to "total delay / 4") before doing the 1st payment.

ℹ️  This program was intended as a joke (while learning Python 🐍).
''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )

myParser.add_argument(
                      '-a',
                      '--amount',
                      metavar='A',
                      type=float,
                      default=123.45,
                      help='the amount to pay',
                      dest='amountToPay'
                      )
myParser.add_argument(
                      '-d',
                      '--days',
                      metavar='D',
                      type=int,
                      default=42,
                      help='days from now until the last payment',
                      dest='daysToTheLastPayment'
                      )
myParser.add_argument(
                      '-n',
                      '--splits',
                      metavar='N',
                      type=int,
                      default=5,
                      help='number of payments',
                      dest='numberOfPayments'
                      )

myArgs = myParser.parse_args()
print('amount to pay =',             myArgs.amountToPay)
print('days to the last payment =',  myArgs.daysToTheLastPayment)
print('number of payments =',        myArgs.numberOfPayments)


cash = slice(totalLength           = myArgs.amountToPay,
             numberOfSlices        = myArgs.numberOfPayments,
             fixedFirstSliceLength = 0,
             minimumSliceLength    = round(myArgs.amountToPay / 100),
             ratio                 = 100
             )
# the "amount / 20" is to have a "fair" minimum value : not too big/small.
# This adds a limitation to this script so that it's not possible to split a debt
# into 20 payments.
#
# Anyway, if we do "min. = amount / 20" while trying to split into a close number
# of payments (18 or 19), each payment ends close to the total / 20, which breaks
# the fun of the whole operation.

delays = slice(totalLength           = myArgs.daysToTheLastPayment,
               numberOfSlices        = myArgs.numberOfPayments,
               fixedFirstSliceLength = round(myArgs.daysToTheLastPayment / 4),
               minimumSliceLength    = 2,
               )
# 'minimumSliceLength = 1' is possible but would allow "1 payment every 1 day",
# which breaks the fun.
#print(cash,   "\t", sum(cash),   "\t", myArgs.amountToPay - sum(cash))
#print(delays, "\t", sum(delays), "\t", myArgs.daysToTheLastPayment - sum(delays))


today = datetime.datetime.now().astimezone()
listOfPayDays = [today]

for i in range(myArgs.numberOfPayments):
    listOfPayDays.append(listOfPayDays[i] + datetime.timedelta(days=delays[i]))


cash.insert(0,'nothing (day 0)') # so that 'cash' and 'listOfPayDays' have
                                 # the same number of elements

print("\n#;date;amount to pay")
[ print("{};{};{}".format(
        i,
        listOfPayDays[i].strftime('%Y-%m-%d'),
        cash[i]))
    for i in range(myArgs.numberOfPayments+1) ]
