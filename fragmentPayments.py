#!/usr/bin/env python3
# -*- coding: utf-8 -*-



#import argparse
#
#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
#
#args = parser.parse_args()
#print(args.accumulate(args.integers))





## source : https://stackoverflow.com/a/50604179/2312935
## principe : on a un livre de N pages. On va insérer n marques-pages aléatoirement dans le livre pour le séparer en n+1 parties de longueurs aléatoires
#import random
#numberToSplit = 11
#initialValuePerSplit = 2
#numberOfSplits = 3
#
#remaining = numberToSplit - initialValuePerSplit * numberOfSplits
## 11-2*3=5
#
#listOfRandomNumbers = sorted([random.randint(0, remaining+1) for i in range(numberOfSplits)])
##                                 0 <= random <= 6                            0, 1, 2 ==> boucle 3 fois
## ==> liste de 3 nombres aléatoires dans le range
#print(listOfRandomNumbers)
## [1, 2, 5]
#
#listOfRandomNumbers.append(remaining)
## on ajoute à la fin :
## liste[dernier] = remaining (5)
#
#listOfRandomNumbers[0] = 0
## on remplace le premier :
## liste[premier] = 0
#
#print(listOfRandomNumbers)
## [0, 2, 5, 5]
#
#print(listOfRandomNumbers[0:numberOfSplits], listOfRandomNumbers[1:numberOfSplits+1])
## liste 1 : [0, 2, 5]
## liste 2 : [2, 5, 5]
#
#result = [j-i+initialValuePerSplit for(i,j) in zip(listOfRandomNumbers[0:numberOfSplits], listOfRandomNumbers[1:numberOfSplits+1])]
## 4, 5, 2
#print(numberToSplit, result)
## 11 [4, 5, 2]
#
## manual
##1, 1, 1
##1, 1, 1, 5
##0, 1, 1, 5
##
##3, 2, 6
#
## executed
##[0, 2, 6]
##[0, 2, 6, 5]
##[0, 2, 6] [2, 6, 5]
##11 [4, 6, 1]






#The method to split any number N into n numbers that sum to N is to :
#- consider a book having N pages
#- place n-1 bookmarks randomly inside the book
#- the n random numbers are the number of pages of each segment
#
#If you had the extra constraint that all splits must be > x :
#- subtract (n*x) from the book length
#- share the remaining
#- then add x to eeach section


import random
numberToSplit = 9873
minimumValuePerSplit = 456
numberOfSplits = 7

remaining = numberToSplit - minimumValuePerSplit * numberOfSplits
print("remaining =", remaining)

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
